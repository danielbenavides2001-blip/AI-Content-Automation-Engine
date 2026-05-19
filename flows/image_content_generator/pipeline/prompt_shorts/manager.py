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
from flows.image_content_generator.pipeline.prompt_shorts.stories import constants as story_constants
from flows.image_content_generator.pipeline.prompt_shorts.stories.models import StoryHandler, StoryIdea
try:
    from flows.image_content_generator.pipeline.prompt_shorts.geography.models import GeographyHandler, GeographyIdea
    from flows.image_content_generator.pipeline.prompt_shorts.geography import constants as geo_constants
    HAS_GEOGRAPHY = True
except ImportError:
    GeographyHandler = None
    GeographyIdea = None
    geo_constants = None
    HAS_GEOGRAPHY = False

from tools.common.messenger import Messenger
from tools.text_generation.gemini import GeminiTextGenerator


class PromptManagerShorts(BasePromptManager):
    """Manager specific to Viral Content (Videos, Riddles, and Stories)."""

    AUDIO_PROMPT: str = story_constants.AUDIO_PROMPT # Defaulting to story audio

    CATEGORIES: Sequence[Type[CategoryHandler]] = [StoryHandler] + ([GeographyHandler] if (HAS_GEOGRAPHY and GeographyHandler) else [])

    def generate_full_story(
        self, content_gen: GeminiTextGenerator, titles_to_avoid: list[str] = [], extra_avoid: str = "", mode: str = "standard"
    ) -> Tuple[BaseIdea, VideoScript, str]:
        """
        Executes the viral generation loop for Story/Geography Reels.
        """
        if mode == "geography":
            if not HAS_GEOGRAPHY or geo_constants is None or GeographyIdea is None:
                raise ValueError("Geography mode is not available in this environment (local-only module missing).")
            category = "geography"
            idea_model = GeographyIdea
            idea_prompt = geo_constants.IDEA_PROMPT_GEOGRAPHY
            script_prompt = geo_constants.SCRIPT_PROMPT_GEOGRAPHY
            series_name = "EnigmaIQ Geografía"
        else:
            category = "stories"
            idea_model = StoryIdea
            idea_prompt = story_constants.IDEA_PROMPT_STORY
            script_prompt = story_constants.SCRIPT_PROMPT
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

        if mode == "geography":
            focus_areas = [
                "BARRERAS GEOGRÁFICAS EXTREMAS: Montañas, desiertos u océanos que bloquean vientos, aíslan países y crean climas de otro planeta.",
                "RÍOS Y CUENCAS COLOSALES: Misterios hídricos, ríos subterráneos, ríos voladores y el impacto de cuencas como el Amazonas.",
                "ZONAS DE PLUVIOSIDAD RÁPIDA Y CLIMAS EXTREMOS: Por qué llueve tanto en el Pacífico sudamericano o cómo el desierto de Atacama quedó seco.",
                "BIODIVERSIDAD Y CORDILLERAS: Cómo las tres cordilleras de los Andes dividen un solo país en mundos ecológicos aislados.",
                "GEOGRAFÍA HISTÓRICA E INSÓLITA: Fronteras absurdas formadas por ríos caprichosos o montañas intransitables."
            ]
        else:
            focus_areas = [
                "MISTERIOS DEL CUERPO HUMANO: Cosas hiper específicas que todos hacemos o sentimos pero nadie sabe por qué.",
                "CURIOSIDADES BIOLÓGICAS EXTREMAS: Comportamientos animales extraños y fascinantes explicados.",
                "MISTERIOS DE CIVILIZACIONES ANTIGUAS: Curiosidades históricas poco conocidas y bizarras.",
                "FENÓMENOS NATURALES BIZARROS: Curiosidades increíbles de la Tierra y el clima.",
                "DATOS PSICOLÓGICOS INQUIETANTES: Curiosidades sobre cómo funciona y nos engaña nuestra propia mente.",
                "SECRETOS DEL UNIVERSO Y EL ESPACIO: Fenómenos cósmicos aterradores o fascinantes explicados de forma sencilla."
            ]
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

        # 3. Dynamic Visual Style Selector
        if mode == "geography":
            styles = [
                "Style: Satellite photography style, realistic earth colors, highly detailed 3D terrain, glowing neon highlights.",
                "Style: Vintage map illustration with modern tech overlay. Sepia map background, bright glowing neon blue and cyan highlights, digital interfaces.",
                "Style: Stylized infographic map. High-contrast dark blue background, vibrant neon borders, sharp glowing vector lines.",
                "Style: Cinematic National Geographic 3D terrain flight. Vibrant natural colors, dramatic lighting, detailed texture."
            ]
        else:
            styles = [
                "Estilo: Hyper-realistic cinematic lighting. Dark moody colors, misty background, high detail, professional photography style.",
                "Estilo: Cinematic National Geographic style documentary. Vibrant colors, ultra-detailed, mysterious and awe-inspiring atmosphere.",
                "Estilo: Vintage anatomical/technical sketch on aged parchment. Sepia ink, detailed, mysterious journal look.",
                "Estilo: Dark digital art. Neon accents, glitchy textures, high contrast, futuristic mystery vibe."
            ]
        selected_style = random.choice(styles)
        
        Messenger.info(f"🎨 Selected Visual Style: {selected_style}")

        # Inyectar el estilo y el área de enfoque
        full_idea_prompt = (
            f"{idea_prompt.format(visual_style=selected_style)}\n\n"
            f"**TEMA CENTRAL OBLIGATORIO:** {selected_area}\n"
            f"**ESTE CONTENIDO ES LA PARTE {next_part}** de la serie '{series_name}'."
        )
        
        idea_data = content_gen.generate_text(
            full_idea_prompt + avoid_msg, 
            idea_model
        )

        # 4. Viral Script / Content Generation
        Messenger.info(f"\n--- Generating Viral {category.upper()} Content: {idea_data.title} ---")
        
        full_script_prompt = (
            script_prompt + 
            f"\n\nIDEA A DESARROLLAR: {idea_data.title}\n"
            f"**ESTILOS VISUALES RECOMENDADOS PARA IMÁGENES/MAPAS:** {selected_style}\n"
        )
        script = content_gen.generate_text(full_script_prompt, GeographyHandler if mode == "geography" else VideoScript)

        # --- BLINDAJE CONTRA BANEOS (TRANS-STORY) ---
        transparency_footer = (
            "\n\n---\n"
            "💡 **Transparencia**: Este contenido narrativo ha sido producido con el apoyo de Inteligencia Artificial para fines educativos y de entretenimiento.\n\n"
            "✨ Creado por el equipo de EnigmaIQ."
        )
        
        # Inyectar el footer en el caption o hook (Blindaje)
        if "caption" in idea_data.model_fields:
            new_val = str(getattr(idea_data, "caption", "")) + transparency_footer
            setattr(idea_data, "caption", new_val)
        elif "hook" in idea_data.model_fields:
            new_val = str(getattr(idea_data, "hook", "")) + transparency_footer
            setattr(idea_data, "hook", new_val)

        return idea_data, script, category
