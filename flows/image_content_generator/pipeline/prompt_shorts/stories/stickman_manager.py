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
        # 1. Select Theme
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

        # 3. Generate and Parse
        Messenger.info(f"   Generating Stickman Story with Theme: {selected_theme}...")
        raw_json = content_gen.generate(full_prompt)
        
        # DEBUG: Log raw response length
        Messenger.info(f"   Raw JSON received (length: {len(raw_json)})")
        
        # Clean JSON
        clean_json = raw_json.strip()
        if "```json" in clean_json:
            clean_json = clean_json.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_json:
            clean_json = clean_json.split("```")[1].split("```")[0].strip()
        
        try:
            # Parse into StickmanNoirIdea
            idea_obj = StickmanNoirIdea.model_validate_json(clean_json)
            # Parse into VideoScript
            script_obj = VideoScript.model_validate_json(clean_json)
            
            if not script_obj.scenes or len(script_obj.scenes) == 0:
                raise ValueError("Gemini returned a script with NO scenes.")

            Messenger.success(f"   Stickman Story parsed successfully: {idea_obj.title} ({len(script_obj.scenes)} scenes)")
            return idea_obj, script_obj
            
        except Exception as e:
            Messenger.error(f"❌ Failed to parse Gemini Stickman JSON: {str(e)}")
            Messenger.info(f"   Problematic JSON: {clean_json[:500]}...")
            raise e
