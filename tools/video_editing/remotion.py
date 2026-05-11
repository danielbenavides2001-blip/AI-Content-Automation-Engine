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
        data: List[Dict[str, Any]],
        composition_id: str = "Subtitles",
    ) -> None:
        """
        Renders a Remotion composition with provided data.
        """
        # 1. Prepare data file
        data_dir = remotion_path / "data"
        data_dir.mkdir(exist_ok=True)
        input_json = data_dir / "input.json"
        
        with open(input_json, "w", encoding="utf-8") as f:
            json.dump({"words": data}, f, indent=2)

        Messenger.info(f"Rendering Remotion composition '{composition_id}'...")
        
        # 2. Run Remotion render
        cmd = [
            "npx.cmd", "remotion", "render",
            "src/index.ts",
            composition_id,
            str(output_path.absolute()),
            f"--props={input_json.absolute()}",
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
