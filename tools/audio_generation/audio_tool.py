import os
import random
import urllib.request
from pathlib import Path
from typing import Any, Optional

from tools.common.base_model import BaseModelTool
from tools.common.messenger import Messenger


# ─── Fallback Music Configuration ────────────────────────────────────────────
MODE_MUSIC_CONFIG = {
    "football": {
        "fallback_subdir": "standard",
        "description": "energetic/sport",
        "url": "https://raw.githubusercontent.com/tannerhelland/free-music/master/mp3/Defiance.mp3",
    },
    "geography": {
        "fallback_subdir": "standard",
        "description": "cinematic/adventure",
        "url": "https://raw.githubusercontent.com/tannerhelland/free-music/master/mp3/Wild%20Waters.mp3",
    },
    "trivias": {
        "fallback_subdir": "standard",
        "description": "cinematic/adventure",
        "url": "https://raw.githubusercontent.com/tannerhelland/free-music/master/mp3/Wild%20Waters.mp3",
    },
    "standard": {
        "fallback_subdir": None,
        "description": "mystery/cinematic",
        "url": "https://raw.githubusercontent.com/tannerhelland/free-music/master/mp3/Ominosity.mp3",
    },
    "stickman": {
        "fallback_subdir": "standard",
        "description": "mystery/dark",
        "url": "https://raw.githubusercontent.com/tannerhelland/free-music/master/mp3/Ominosity.mp3",
    },
}

DEFAULT_MODE = "standard"


class AudioTool(BaseModelTool):
    """
    Tool for audio-related operations, like background music selection.

    Supports per-mode subdirectories inside bg_music_dir:
        bg-music/
            football/   ← energetic/sport tracks
            standard/   ← mystery/cinematic tracks
            geography/  ← adventure/epic tracks

    If a mode subdirectory is empty, attempts to auto-download a high-quality
    Creative Commons track from a raw repository CDN, and falls back to standard
    tracks as a last resort.
    """

    bg_music_dir: Path

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    # ─── Public API ──────────────────────────────────────────────────────────

    def get_random_audio(self, mode: str = "standard") -> Optional[Path]:
        """
        Returns a random background music file for the given pipeline mode.

        Search order:
        1. bg_music_dir/<mode>/  subdirectory
        2. Auto-download a high-quality genre-specific MP3 from public CC CDN
        3. bg_music_dir/<fallback_mode>/  (if configured)
        4. bg_music_dir/  root (legacy)
        """
        mode = mode.lower() if mode else DEFAULT_MODE
        config = MODE_MUSIC_CONFIG.get(mode, MODE_MUSIC_CONFIG[DEFAULT_MODE])

        Messenger.info(f"🎵 Selecting background music for mode: {mode.upper()} ({config['description']})")

        # 1. Try mode-specific subdir
        mode_dir = self.bg_music_dir / mode
        selected = self._pick_from_dir(mode_dir)
        if selected:
            return selected

        # 2. Try raw repository CDN auto-download to match the desired style
        Messenger.info(f"   ↳ No local music found in {mode}/. Attempting raw CDN auto-download...")
        downloaded = self._auto_download_fallback(mode, config)
        if downloaded:
            return downloaded

        # 3. Try fallback subdir
        fallback = config.get("fallback_subdir")
        if fallback:
            fallback_dir = self.bg_music_dir / fallback
            selected = self._pick_from_dir(fallback_dir)
            if selected:
                Messenger.info(f"   ↳ CDN download failed. Using fallback subdir: {fallback}/")
                return selected

        # 4. Try root dir (legacy behaviour)
        selected = self._pick_from_dir(self.bg_music_dir)
        if selected:
            Messenger.info("   ↳ Using root bg-music dir (legacy)")
            return selected

        Messenger.error("❌ No background music available. Step 6 will be skipped.")
        return None

    # ─── Private helpers ─────────────────────────────────────────────────────

    def _pick_from_dir(self, directory: Path) -> Optional[Path]:
        """Returns a random audio file from directory, or None if empty/missing."""
        if not directory.exists():
            return None
        extensions = {".wav", ".mp3", ".aac", ".m4a", ".ogg"}
        files = [
            f for f in directory.iterdir()
            if f.is_file() and f.suffix.lower() in extensions
        ]
        if not files:
            return None
        selected = random.choice(files)
        Messenger.info(f"   ✅ Selected: {selected.parent.name}/{selected.name}")
        return selected

    def _auto_download_fallback(self, mode: str, config: dict) -> Optional[Path]:
        """
        Downloads a verified high-quality royalty-free MP3 track from a public
        Creative Commons CDN and saves it to the appropriate subdirectory.
        """
        url = config.get("url")
        if not url:
            return None

        # Clean name from URL
        filename = url.split("/")[-1].replace("%20", "_")
        out_dir = self.bg_music_dir / mode
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / filename

        try:
            Messenger.info(f"   ⬇️ Downloading high-quality MP3: {filename} ...")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as r, open(out_file, "wb") as f:
                f.write(r.read())

            if out_file.exists() and out_file.stat().st_size > 100000:
                Messenger.success(f"   ✅ Auto-downloaded: {out_file.name}")
                return out_file
            else:
                if out_file.exists():
                    out_file.unlink()
                return None

        except Exception as e:
            Messenger.warning(f"Raw CDN music download failed: {e}")
            if out_file.exists():
                out_file.unlink()
            return None
