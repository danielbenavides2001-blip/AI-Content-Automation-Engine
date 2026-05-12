import random
from typing import Tuple, List, ClassVar

from flows.image_content_generator.pipeline.prompt_base.manager import BasePromptManager
from flows.image_content_generator.pipeline.prompt_base.models import BaseIdea, VideoScript, Scene
from flows.image_content_generator.pipeline.prompt_shorts.stories import stickman_constants
from flows.image_content_generator.pipeline.prompt_base.models import StickmanNoirIdea
from tools.text_generation.gemini import GeminiTextGenerator


class StickmanNoirManager(BasePromptManager):
    """
    Manager for the high-quality Stickman Noir format (Option 1).
    Focuses on behavioral psychology and noir aesthetics.
    """
    IDEA_PROMPT: ClassVar[str] = stickman_constants.IDEA_PROMPT_STICKMAN
    AUDIO_PROMPT: ClassVar[str] = stickman_constants.AUDIO_PROMPT_STICKMAN

    def generate_full_story(
        self, content_gen: GeminiTextGenerator, titles_to_avoid: List[str] = [], extra_avoid: str = ""
    ) -> Tuple[StickmanNoirIdea, VideoScript]:
        """
        Generates a complete Stickman Noir cycle: Idea + Script.
        """
        # 1. Select Theme and Symbol (Originality Motor)
        themes = ["Autoengaño", "Envidia", "Ambición tóxica", "Procrastinación", "Duelo", "Validación externa", "Ego", "Disciplina", "Silencio", "Intuición"]
        selected_theme = random.choice(themes)
        
        # 2. Format the prompt
        avoid_msg = extra_avoid
        if titles_to_avoid:
            avoid_msg += "\n\n**TEMAS YA USADOS:**\n" + "\n".join([f"- {t}" for t in titles_to_avoid[-15:]])

        full_prompt = self.IDEA_PROMPT.format(
            selected_area=selected_theme,
            avoid_msg=avoid_msg
        )

        # 3. Generate Idea and Script in ONE call for maximum coherence
        # We use VideoScript as the primary model, but we need it to include the Idea fields.
        # Actually, let's just generate the JSON and parse it manually into both models.
        
        raw_json = content_gen.generate(full_prompt)
        
        # Clean JSON if it's wrapped in markdown
        clean_json = raw_json.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
        clean_json = clean_json.strip()

        # Parse into StickmanNoirIdea
        idea_obj = StickmanNoirIdea.model_validate_json(clean_json)
        
        # Parse into VideoScript
        script_obj = VideoScript.model_validate_json(clean_json)
        
        # Validation: Ensure exactly 4 scenes
        if len(script_obj.scenes) != 4:
            # Fallback or retry logic could go here, but for now we trust Gemini
            pass

        return idea_obj, script_obj
