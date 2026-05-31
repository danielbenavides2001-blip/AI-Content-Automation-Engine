import os
import random
import urllib.request
import urllib.parse
import json
from pathlib import Path
from typing import Any, Optional

from tools.common.base_model import BaseModelTool
from tools.common.messenger import Messenger


# ─── Pixabay search tags per mode ────────────────────────────────────────────
MODE_MUSIC_CONFIG = {
    "football": {
        "tags": ["sport", "energetic", "upbeat", "action"],
        "fallback_subdir": "standard",  # if football/ is empty, use standard/
        "description": "energetic/sport",
    },
    "geography": {
        "tags": ["cinematic", "adventure", "epic", "world"],
        "fallback_subdir": "standard",
        "description": "cinematic/adventure",
    },
    "standard": {
        "tags": ["mystery", "dark", "cinematic", "suspense"],
        "fallback_subdir": None,
        "description": "mystery/cinematic",
    },
    "stickman": {
        "tags": ["mystery", "dark", "cinematic", "suspense"],
        "fallback_subdir": "standard",
        "description": "mystery/dark",
    },
}

# Default when mode is unknown
DEFAULT_MODE = "standard"


class AudioTool(BaseModelTool):
    """
    Tool for audio-related operations.

    Supports per-mode subdirectories inside bg_music_dir:
        bg-music/
            football/   ← energetic/sport tracks
            standard/   ← mystery/cinematic tracks
            geography/  ← adventure/epic tracks

    If a mode subdirectory is empty or missing, falls back to the root
    bg_music_dir (original behaviour) and optionally auto-downloads a
    track from the Pixabay Music API.
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
        2. Auto-download from Pixabay API (if PIXABAY_API_KEY is set)
        3. bg_music_dir/<fallback_mode>/  (if configured)
        4. bg_music_dir/  root (legacy – stickman-bg.WAV lives here)
        """
        mode = mode.lower() if mode else DEFAULT_MODE
        config = MODE_MUSIC_CONFIG.get(mode, MODE_MUSIC_CONFIG[DEFAULT_MODE])

        Messenger.info(f"🎵 Selecting background music for mode: {mode.upper()} ({config['description']})")

        # 1. Try mode-specific subdir
        mode_dir = self.bg_music_dir / mode
        selected = self._pick_from_dir(mode_dir)
        if selected:
            return selected

        # 2. Try Pixabay auto-download first to match the desired style
        Messenger.info(f"   ↳ No local music found in {mode}/. Attempting Pixabay auto-download...")
        downloaded = self._auto_download_from_pixabay(mode, config)
        if downloaded:
            return downloaded

        # 3. Try fallback subdir
        fallback = config.get("fallback_subdir")
        if fallback:
            fallback_dir = self.bg_music_dir / fallback
            selected = self._pick_from_dir(fallback_dir)
            if selected:
                Messenger.info(f"   ↳ Pixabay download failed/skipped. Using fallback subdir: {fallback}/")
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

    def _auto_download_from_pixabay(self, mode: str, config: dict) -> Optional[Path]:
        """
        Downloads a random royalty-free track from Pixabay Music API
        and saves it to the appropriate subdirectory.
        Requires PIXABAY_API_KEY environment variable.
        """
        api_key = os.getenv("PIXABAY_API_KEY")
        if not api_key:
            Messenger.warning("PIXABAY_API_KEY not set — cannot auto-download music.")
            return None

        # Pick a random search tag for variety
        tags = config.get("tags", ["cinematic"])
        tag = random.choice(tags)

        try:
            params = urllib.parse.urlencode({
                "key": api_key,
                "q": tag,
                "media_type": "music",
                "per_page": 20,
                "safesearch": "true",
            })
            url = f"https://pixabay.com/api/?{params}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())

            hits = data.get("hits", [])
            if not hits:
                Messenger.warning(f"Pixabay returned no music for tag: '{tag}'")
                return None

            # Pick a random track from results
            track = random.choice(hits)
            audio_url = track.get("audioURL") or track.get("largeImageURL")
            if not audio_url:
                Messenger.warning("Pixabay track has no audioURL.")
                return None

            # Save to mode subdir
            out_dir = self.bg_music_dir / mode
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"pixabay_{tag}_{track.get('id', 'unknown')}.mp3"

            Messenger.info(f"   ⬇️ Downloading Pixabay track: {out_file.name} ...")
            req_audio = urllib.request.Request(audio_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req_audio, timeout=60) as r, open(out_file, "wb") as f:
                f.write(r.read())

            if out_file.exists() and out_file.stat().st_size > 10000:
                Messenger.success(f"   ✅ Auto-downloaded: {out_file.name}")
                return out_file
            else:
                out_file.unlink(missing_ok=True)
                return None

        except Exception as e:
            Messenger.warning(f"Pixabay music auto-download failed: {e}")
            return None
