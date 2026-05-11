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
        force_type = os.getenv("FORCE_POST_TYPE")
        
        if force_type == "2":
            idea_model = InteractionImageIdea
        elif force_type == "1":
            idea_model = MindsetFinanceIdea
        else:
            # Si no hay fuerza, usamos el azar pero coordinado
            idea_model = random.choice(FinanceHandler.idea_variants)
        
        idea_prompt = getattr(idea_model, "IDEA_PROMPT", finance_constants.IDEA_PROMPT_MINDSET)

        # 2. Part Counter for "EnigmaIQ"
        series_name = "EnigmaIQ"
        
        # Scan both the list and the extra_avoid string for the series name
        parts_count = sum(1 for t in titles_to_avoid if series_name in str(t))
        if extra_avoid and series_name in extra_avoid:
            import re
            parts_found = re.findall(rf"{series_name} - Parte (\d+)", extra_avoid)
            if parts_found:
                max_part = max(int(p) for p in parts_found)
                parts_count = max(parts_count, max_part)

        next_part = parts_count + 1
        Messenger.info(f"🎞️ Series: {series_name} | Next Part: {next_part}")

        # 3. Idea Generation with Focus Area Diversity (NEW DIVERSITY ENGINE)
        focus_areas = [
            "BIOHACKING & LONGEVITY (Ayuno intermitente, nootrópicos, protocolos de sueño, optimización celular)",
            "IA & PRODUCTIVIDAD (Side-hustles con IA, automatización de tareas, ahorro de tiempo, herramientas disruptivas)",
            "FINANZAS DE GUERRILLA (Minimalismo financiero, inversión en micro-acciones, hacks de ahorro extremo)",
            "PSICOLOGÍA OSCURA (Lenguaje corporal, detección de mentiras, red flags, persuasión en negocios)",
            "URBAN HOMESTEADING & TECH (Huertos hidropónicos, energía solar DIY, sustentabilidad tecnológica)"
        ]
        # Eliminamos temporalmente 'Psicología' para forzar temas técnicos y frescos
        selected_area = random.choice(focus_areas)
        Messenger.info(f"🎯 Random Focus Area: {selected_area}")

        avoid_msg = ""
        banned_words = "Pobre, Rico, Mentalidad, Escasez, Abundancia, Mindset, Millonario"
        if extra_avoid:
            avoid_msg = f"\n\n🚨 **REGLA DE ORO DE NO REPETICIÓN:** 🚨\nEstá PROHIBIDO repetir temas anteriores como:\n{extra_avoid}\n\n🚫 **PALABRAS PROHIBIDAS (NO USAR):** {banned_words}"
        elif titles_to_avoid:
            avoid_list_str = "\n- ".join(titles_to_avoid)
            avoid_msg = (
                f"\n\n🚨 **REGLA DE ORO DE NO REPETICIÓN:** 🚨\n"
                f"Está ESTRICTAMENTE PROHIBIDO repetir cualquiera de estos temas o conceptos:\n- {avoid_list_str}\n\n"
                f"🚫 **PALABRAS PROHIBIDAS (NO USAR):** {banned_words}"
            )

        # Inyectar el número de parte y el área de enfoque
        full_idea_prompt = (
            f"{idea_prompt}\n\n"
            f"**TEMA CENTRAL OBLIGATORIO:** {selected_area}\n"
            f"**ESTE CONTENIDO ES LA PARTE {next_part}** de la serie '{series_name}'."
        )
        
        idea_data = content_gen.generate_text(
            full_idea_prompt + avoid_msg, 
            idea_model
        )

        # 3. Viral Script / Content Generation
        is_riddle = (idea_model == InteractionImageIdea)
        Messenger.info(f"\n--- Generating Viral Content ({'RIDDLE' if is_riddle else 'VIDEO'}): {idea_data.title} ---")
        
        if is_riddle:
            # Extraer el prompt real generado por la IA (ahora campo de primer nivel)
            real_prompt = getattr(idea_data, "image_prompt", idea_data.title)
            
            script = VideoScript(
                scenes=[{
                    "scene_number": 1,
                    "narration": "", 
                    "image_prompt": real_prompt
                }]
            )
        else:
            full_script_prompt = (
                finance_constants.SCRIPT_PROMPT + 
                f"\n\nIDEA A DESARROLLAR: {idea_data.title}\n"
                f"RECUERDA: Tono barítono, pausado, 4 escenas, personaje Stickman Blanco (minimalista, fondo crema)."
            )
            script = content_gen.generate_text(full_script_prompt, VideoScript)

        return idea_data, script, category
