from typing import Sequence, Tuple, Type, Optional
import random
import os

from flows.image_content_generator.pipeline.prompt_base.manager import BasePromptManager
from flows.image_content_generator.pipeline.prompt_base.models import (
    BaseIdea,
    CategoryHandler,
    VideoScript,
    ImagePrompt,
)
from flows.image_content_generator.pipeline.prompt_shorts.finances import (
    constants as finance_constants,
)
from flows.image_content_generator.pipeline.prompt_shorts.finances.models import FinanceHandler, MindsetFinanceIdea, InteractionImageIdea
from tools.common.messenger import Messenger
from tools.text_generation.gemini import GeminiTextGenerator


class PromptManagerShorts(BasePromptManager):
    """Manager specific to Viral Stickman Finance Content (Videos & Riddles)."""

    AUDIO_PROMPT: str = finance_constants.AUDIO_PROMPT

    CATEGORIES: Sequence[Type[CategoryHandler]] = [
        FinanceHandler,
    ]

    def generate_full_story(
        self, content_gen: GeminiTextGenerator, titles_to_avoid: list[str] = [], extra_avoid: str = ""
    ) -> Tuple[BaseIdea, VideoScript, str]:
        """
        Executes the viral generation loop for either Video or Interaction Image.
        """
        category = "finances"
        
        # 1. Determinamos el modelo de idea basado en la intención del sistema
        # Si FORCE_POST_TYPE=2 o el contador indica imagen, usamos InteractionImageIdea
        # Si FORCE_POST_TYPE=1 o el contador indica video, usamos MindsetFinanceIdea
        force_type = os.getenv("FORCE_POST_TYPE")
        
        if force_type == "2":
            idea_model = InteractionImageIdea
        elif force_type == "1":
            idea_model = MindsetFinanceIdea
        else:
            # Si no hay fuerza, usamos el azar pero coordinado
            idea_model = random.choice(FinanceHandler.idea_variants)
        
        idea_prompt = getattr(idea_model, "IDEA_PROMPT", finance_constants.IDEA_PROMPT_MINDSET)

        # 2. Part Counter for "Formas cochinas de ganar dinero"
        series_name = "Formas cochinas de ganar dinero"
        
        # Scan both the list and the extra_avoid string for the series name
        parts_count = sum(1 for t in titles_to_avoid if series_name in str(t))
        if extra_avoid and series_name in extra_avoid:
            # If we don't have a list but we have the string, try to find the max part
            import re
            parts_found = re.findall(rf"{series_name} - Parte (\d+)", extra_avoid)
            if parts_found:
                max_part = max(int(p) for p in parts_found)
                parts_count = max(parts_count, max_part)

        next_part = parts_count + 1
        
        Messenger.info(f"🎞️ Series: {series_name} | Next Part: {next_part}")

        # 3. Idea Generation with Strict Avoidance (THE GOLDEN RULE)
        avoid_msg = ""
        if extra_avoid:
            # extra_avoid usually contains a formatted list of topics/metaphors
            avoid_msg = f"\n\n🚨 **REGLA DE ORO DE NO REPETICIÓN:** 🚨\n{extra_avoid}"
        elif titles_to_avoid:
            avoid_list_str = "\n- ".join(titles_to_avoid)
            avoid_msg = (
                f"\n\n🚨 **REGLA DE ORO DE NO REPETICIÓN:** 🚨\n"
                f"Está ESTRICTAMENTE PROHIBIDO repetir cualquiera de estos temas o conceptos:\n- {avoid_list_str}\n\n"
                f"Tu misión es crear contenido 100% ÚNICO y FRESCO."
            )

        # Inyectar el número de parte en el prompt
        full_idea_prompt = f"{idea_prompt}\n\n**ESTE VIDEO ES LA PARTE {next_part}** de la serie '{series_name}'."
        
        idea_data = content_gen.generate_text(
            full_idea_prompt + avoid_msg, 
            idea_model
        )

        # Force title format to maintain counter tracking
        prefix = f"[{series_name} - Parte {next_part}]"
        if prefix not in idea_data.title:
            idea_data.title = f"{prefix} {idea_data.title}"

        # 3. Viral Script / Content Generation
        is_riddle = (idea_model == InteractionImageIdea)
        Messenger.info(f"\n--- Generating Viral Content ({'RIDDLE' if is_riddle else 'VIDEO'}): {idea_data.title} ---")
        
        if is_riddle:
            # Para imágenes de interacción, el "script" es un objeto simplificado
            full_script_prompt = (
                finance_constants.IMAGE_INTERACTION_PROMPT + 
                f"\n\nIDEA A DESARROLLAR: {idea_data.title}\n"
                f"RECUERDA: Stickman minimalista, fondo blanco, texto corto y provocador."
            )
            # FIX PYDANTIC: Crear el objeto con la estructura correcta (image_prompt es string)
            script = VideoScript(
                scenes=[{
                    "scene_number": 1,
                    "narration": "", 
                    "image_prompt": idea_data.title
                }]
            )
        else:
            # Para videos animados
            full_script_prompt = (
                finance_constants.SCRIPT_PROMPT + 
                f"\n\nESTE VIDEO ES LA PARTE {next_part} de la serie '{series_name}'.\n"
                f"IDEA A DESARROLLAR: {idea_data.title}\n"
                f"RECUERDA: Tono cínico, profesional, 4 escenas, personaje Stickman Noir (traje, sombrero, gafas)."
            )
            script = content_gen.generate_text(full_script_prompt, VideoScript)

        return idea_data, script, category
