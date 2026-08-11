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
from flows.image_content_generator.pipeline.prompt_shorts.siete_niveles.models import SieteNivelesHandler, SieteNivelesIdea
from flows.image_content_generator.pipeline.prompt_shorts.siete_niveles import constants as sn_constants


class PromptManagerShorts(BasePromptManager):
    """Manager specific to Viral Content (Videos, Riddles, and Stories)."""

    AUDIO_PROMPT: str = story_constants.AUDIO_PROMPT # Defaulting to story audio

    CATEGORIES: Sequence[Type[CategoryHandler]] = (
        [StoryHandler]
        + ([GeographyHandler] if (HAS_GEOGRAPHY and GeographyHandler) else [])
        + [SieteNivelesHandler]
    )

    def generate_full_story(
        self, content_gen: GeminiTextGenerator, titles_to_avoid: list[str] = [], extra_avoid: str = "", mode: str = "standard"
    ) -> Tuple[BaseIdea, VideoScript, str]:
        """
        Executes the viral generation loop for Story/Geography/Trivias Reels.
        """
        if mode == "geography":
            if not HAS_GEOGRAPHY or geo_constants is None or GeographyIdea is None:
                raise ValueError("Geography mode is not available in this environment (local-only module missing).")
            category = "geography"
            idea_model = GeographyIdea
            idea_prompt = geo_constants.IDEA_PROMPT_GEOGRAPHY
            script_prompt = geo_constants.SCRIPT_PROMPT_GEOGRAPHY
            series_name = "EnigmaIQ Geografía"
        elif mode == "siete_niveles":
            category = "siete_niveles"
            idea_model = SieteNivelesIdea
            idea_prompt = sn_constants.IDEA_PROMPT_SIETE_NIVELES
            script_prompt = sn_constants.SCRIPT_PROMPT_SIETE_NIVELES
            series_name = "EnigmaIQ 7 Niveles"
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
        elif mode == "siete_niveles":
            focus_areas = sn_constants.FOCUS_AREAS_SIETE_NIVELES
        else:
            focus_areas = [
                "CURIOSIDADES DE LOS TERREMOTOS: Datos científicos asombrosos sobre cómo se producen los sismos, luces de terremoto, y la inmensa energía liberada que la geología sigue estudiando.",
                "LOS MAYORES SISMOS DE LA HISTORIA: Relatos impactantes de los sismos de mayor magnitud que han cambiado la geografía del planeta y cómo la humanidad se adaptó a ellos.",
                "HISTORIAS DE TERREMOTOS EN LATINOAMÉRICA: Eventos históricos, milagros de supervivencia y la increíble resiliencia de la población ocurrida durante los sismos más recordados en América Latina (Chile, México, Perú).",
                "TERREMOTOS EN COLOMBIA: Un repaso por la historia geológica y sísmica de Colombia, por qué tiembla tanto y los eventos naturales más memorables que han marcado al país.",
                "TERREMOTO EN COLOMBIA (AGOSTO 2026): El impresionante sismo de magnitud 7.4 con epicentro en San José del Palmar, Chocó. Historias de impacto, cómo reaccionaron las ciudades principales y la inmensa fuerza de la naturaleza en vivo."
            ]
        selected_area = random.choice(focus_areas)
        Messenger.info(f"🎯 Random Focus Area: {selected_area}")

        avoid_msg = ""
        banned_words = "Pobre, Rico, Mentalidad, Escasez, Abundancia, Mindset, Millonario"
        
        unsafe_words = ["muerte", "mortal", "masacre", "asesin", "mata", "letal", "tragedia", "destru", "sangre", "gore", "cadáver", "herido", "suicidi", "manson", "infierno", "terror", "violaci"]
        
        # Filtramos titles_to_avoid para no enviar palabras violentas del pasado a la IA
        combined_avoid = [t for t in titles_to_avoid if not any(w in str(t).lower() for w in unsafe_words)]
        
        # LÍMITE CRÍTICO DE MEMORIA: Ahora que usamos gemini-2.5-flash, podemos enviar un historial mucho más largo.
        # Pasamos los últimos 150 temas para asegurar máxima variedad y evitar repeticiones a toda costa.
        combined_avoid = combined_avoid[-150:]
        
        if extra_avoid:
            # extra_avoid already comes as a formatted string from get_recent_topics (ya filtrado)
            combined_avoid.append(extra_avoid)
            
        if combined_avoid:
            avoid_list_str = "\n".join([str(t) for t in combined_avoid])
            avoid_msg = (
                f"\n\n🚨 **REGLA DE ORO DE NO REPETICIÓN ABSOLUTA:** 🚨\n"
                f"Está ESTRICTAMENTE PROHIBIDO repetir CUALQUIERA de estos temas, historias o conceptos que ya fueron publicados:\n"
                f"{avoid_list_str}\n\n"
                f"Si generas una historia similar a las anteriores, el sistema fallará. DEBES INVENTAR UN TEMA COMPLETAMENTE NUEVO.\n"
                f"🚫 **PALABRAS PROHIBIDAS (NO USAR):** {banned_words}"
            )

        # 3. Dynamic Visual Style Selector (With high diversity to prevent template-like feel)
        color_schemes = [
            "Palette: Rich saturated organic colors with golden accents.",
            "Palette: Cool high-contrast neon blues, cyans, and emerald greens on deep black backgrounds.",
            "Palette: Warm nostalgic sepias, terracotta, and deep forest greens.",
            "Palette: Moody dark cinematic monochrome with a single sharp splash of crimson red.",
            "Palette: Vintage retro pastel tones (cream, warm teal, faded copper, and soft amber).",
            "Palette: Dramatic dark slate grey, textured carbon black, and vibrant electric orange highlights.",
        ]
        
        compositions = [
            "Composition: Dynamic asymmetric layout with diagonal splitting lines, placing key elements in different quadrants each scene.",
            "Composition: Close-up macro focus on key historical objects in the foreground, with highly detailed backgrounds showing action.",
            "Composition: Mixed-media layered collage, alternating overlapping frames, Polaroid borders, and torn paper edges.",
            "Composition: Symmetrical blueprint-like technical overlay, clean lines, and glowing focal points.",
            "Composition: Cinematic wide-angle view, deep shadows, and high-contrast dramatic side-lighting.",
        ]

        color_factor = random.choice(color_schemes)
        comp_factor = random.choice(compositions)

        if mode == "geography":
            styles = [
                "Base Style: Detailed 3D Satellite photography style, realistic earth colors, highly detailed terrain relief, and glowing neon indicators.",
                "Base Style: Vintage 19th-century cartography illustration with a modern technological overlay. Aged sepia map background mixed with bright glowing cyan vector highlights.",
                "Base Style: Stylized topographic infographic map. High-contrast dark navy background with vibrant glowing yellow and neon green border contours.",
                "Base Style: Dramatic cinematic National Geographic flight. Deep natural green and ocean blue colors, dramatic morning sun rays, and ultra-detailed relief textures.",
            ]
        elif mode == "siete_niveles":
            styles = [
                "Base Style: Dark cinematic documentary style. Deep shadows, dramatic side-lighting, mysterious atmosphere, rich textures and volumetric fog effects.",
                "Base Style: High-contrast mystery magazine aesthetic. Dark backgrounds with glowing golden accents, bold typography-inspired compositions, dramatic spot lighting.",
                "Base Style: Moody National Geographic explorer style. Warm earthy tones, vintage map textures, compass and parchment overlays, explorer's journal aesthetic.",
                "Base Style: Dark sci-fi documentary style. Neon cyan and deep blue palette, holographic grid overlays, sleek data visualization elements, futuristic yet grounded.",
            ]
        else:
            styles = [
                "Base Estilo: Hyper-realistic cinematic documentary footage. Sharp focus, natural earthy colors, high detail, professional photography style capturing raw nature.",
                "Base Estilo: Cinematic National Geographic style documentary. Vibrant colors, ultra-detailed textures of earth and structures, realistic awe-inspiring atmosphere.",
                "Base Estilo: Highly detailed 3D historical reconstruction. Photorealistic rendering, cinematic lighting, dust and atmospheric depth, intense realism.",
                "Base Estilo: Dramatic photojournalism style. High contrast, raw emotion, gritty realism, capturing the raw power of geological forces.",
                "Base Estilo: Epic cinematic realism. Sweeping landscapes, dramatic natural lighting, hyper-detailed geological formations, immersive and powerful."
            ]
        
        base_style = random.choice(styles)
        # Assemble a fully unique dynamic styling guide
        selected_style = f"{base_style} | {color_factor} | {comp_factor} | Ensure you strictly vary the order of visual elements, foreground objects, and layouts across all scenes so no two scenes look identical or templated."
        
        Messenger.info(f"🎨 Selected Visual Style: {selected_style}")

        # Inyectar el estilo y el área de enfoque
        full_idea_prompt = (
            f"{idea_prompt.format(visual_style=selected_style)}\n\n"
            f"**TEMA CENTRAL OBLIGATORIO:** {selected_area}\n"
            f"**ESTE CONTENIDO IS LA PARTE {next_part}** de la serie '{series_name}'."
        )
        
        idea_data = content_gen.generate_text(
            full_idea_prompt + avoid_msg, 
            idea_model
        )

        # 4. Viral Script / Content Generation
        Messenger.info(f"\n--- Generating Viral {category.upper()} Content: {idea_data.title} ---")
        
        if mode == "siete_niveles":
            full_script_prompt = (
                script_prompt +
                f"\n\nIDEA A DESARROLLAR: {idea_data.title}\n"
                f"INTRIGUE HEADER DE LA IDEA: {getattr(idea_data, 'intrigue_header', '')}\n"
                f"**ESTILOS VISUALES RECOMENDADOS:** {selected_style}\n"
                f"\n\n**DATOS COMPLETOS DE LA IDEA (CONTEXTO):**\n{idea_data.model_dump_json(indent=2)}\n"
            )
        else:
            full_script_prompt = (
                script_prompt + 
                f"\n\nIDEA A DESARROLLAR: {idea_data.title}\n"
                f"**ESTILOS VISUALES RECOMENDADOS PARA IMÁGENES/MAPAS:** {selected_style}\n"
            )
        if mode == "geography":
            script_schema = GeographyHandler
        elif mode == "siete_niveles":
            script_schema = SieteNivelesHandler
        else:
            script_schema = VideoScript
        script = content_gen.generate_text(full_script_prompt, script_schema)

        # --- BLINDAJE CONTRA BANEOS (TRANS-STORY) ---
        creator_team = "equipo de EnigmaIQ"
        transparency_footer = (
            f"\n\n---\n"
            f"💡 **Transparencia**: Este contenido narrativo ha sido producido con el apoyo de Inteligencia Artificial para fines educativos y de entretenimiento.\n\n"
            f"✨ Creado por el {creator_team}."
        )
        
        # Inyectar el footer en el caption o hook (Blindaje)
        if "caption" in idea_data.model_fields:
            new_val = str(getattr(idea_data, "caption", "")) + transparency_footer
            setattr(idea_data, "caption", new_val)
        elif "hook" in idea_data.model_fields:
            new_val = str(getattr(idea_data, "hook", "")) + transparency_footer
            setattr(idea_data, "hook", new_val)

        return idea_data, script, category
