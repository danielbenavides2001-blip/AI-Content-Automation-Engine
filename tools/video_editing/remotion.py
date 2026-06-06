import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any

from tools.common.base_model import BaseModelTool
from tools.common.messenger import Messenger

class RemotionTool(BaseModelTool):
    """
    Tool for rendering videos using Remotion CLI.
    """

    def render_subtitles(
        self,
        remotion_path: Path,
        output_path: Path,
        words: List[Dict[str, Any]],
        composition_id: str = "Subtitles",
        intrigue_header: str = None,
        level_markers: List[Dict[str, Any]] = None,
    ) -> None:
        """
        Renders a Remotion composition with provided data.
        """
        # 1. Prepare data file
        data_dir = remotion_path / "data"
        data_dir.mkdir(exist_ok=True)
        input_json = data_dir / "input.json"
        
        payload = {"words": words}
        if intrigue_header:
            payload["intrigueHeader"] = intrigue_header
        if level_markers:
            payload["levelMarkers"] = level_markers

        with open(input_json, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        Messenger.info(f"Rendering Remotion composition '{composition_id}'...")
        
        # 2. Run Remotion render
        import platform
        import tempfile
        npx_cmd = "npx.cmd" if platform.system() == "Windows" else "npx"
        
        # If output has no extension or is a pattern, it's a sequence
        is_sequence = output_path.suffix not in ['.mp4', '.webm', '.mov', '.mkv']
        
        # Remotion path parser breaks on paths containing '.' in dir names (e.g., .gemini).
        # Use a temp dir without dots and copy result afterward.
        use_temp = "." in str(output_path.resolve().parent)
        if use_temp:
            temp_out = Path(tempfile.mkdtemp(prefix="remotion_"))
        else:
            temp_out = output_path

        # Ensure parent of final output exists
        if not use_temp:
            output_path.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            npx_cmd, "remotion", "render",
            "src/index.ts",
            composition_id,
            str(temp_out.absolute()),
            f"--props={input_json.absolute()}",
        ]

        if is_sequence:
            cmd.append("--sequence")
            cmd.append("--image-sequence-pattern=[frame].[ext]")
        else:
            cmd.append("--codec=vp9")

        try:
            subprocess.run(
                cmd,
                cwd=str(remotion_path),
                capture_output=True,
                text=True,
                check=True
            )
            Messenger.success(f"Remotion render completed: {output_path.name}")
        except subprocess.CalledProcessError as e:
            Messenger.error(f"Remotion failed: {e.stderr}")
            raise RuntimeError(f"Remotion rendering failed: {e.stderr}")

        # Copy result from temp dir to actual output
        if use_temp:
            if is_sequence:
                output_path.mkdir(parents=True, exist_ok=True)
                for item in temp_out.iterdir():
                    dest = output_path / item.name
                    if dest.exists():
                        dest.unlink()
                    item.rename(dest)
            else:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                if output_path.exists():
                    output_path.unlink()
                temp_out.rename(output_path)
            temp_out.rmdir()

    def render_composition(
        self,
        remotion_path: Path,
        output_path: Path,
        composition_id: str,
        props: Dict[str, Any]
    ) -> None:
        """
        Renders any Remotion composition with the given props.
        """
        data_dir = remotion_path / "data"
        data_dir.mkdir(exist_ok=True)
        input_json = data_dir / f"input_{composition_id.lower()}.json"
        
        with open(input_json, "w", encoding="utf-8") as f:
            json.dump(props, f, indent=2)

        Messenger.info(f"Rendering Remotion composition '{composition_id}'...")
        
        import platform
        npx_cmd = "npx.cmd" if platform.system() == "Windows" else "npx"
        
        cmd = [
            npx_cmd, "remotion", "render",
            "src/index.ts",
            composition_id,
            str(output_path.absolute()),
            f"--props={input_json.absolute()}",
            "--codec=h264",
            "-y"
        ]

        try:
            subprocess.run(
                cmd,
                cwd=str(remotion_path),
                capture_output=True,
                text=True,
                check=True
            )
            Messenger.success(f"Remotion render completed: {output_path.name}")
        except subprocess.CalledProcessError as e:
            Messenger.error(f"Remotion failed: {e.stderr}")
            raise RuntimeError(f"Remotion rendering failed: {e.stderr}")
