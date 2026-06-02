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
from flows.image_content_generator.pipeline.prompt_shorts.trivias.models import TriviasHandler, TriviaIdea
from flows.image_content_generator.pipeline.prompt_shorts.trivias import constants as trivia_constants


class PromptManagerShorts(BasePromptManager):
    """Manager specific to Viral Content (Videos, Riddles, and Stories)."""

    AUDIO_PROMPT: str = story_constants.AUDIO_PROMPT # Defaulting to story audio

    CATEGORIES: Sequence[Type[CategoryHandler]] = (
        [StoryHandler]
        + ([GeographyHandler] if (HAS_GEOGRAPHY and GeographyHandler) else [])
        + [TriviasHandler]
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
        elif mode == "trivias":
            category = "trivias"
            idea_model = TriviaIdea
            idea_prompt = trivia_constants.IDEA_PROMPT_TRIVIAS
            script_prompt = trivia_constants.SCRIPT_PROMPT_TRIVIAS
            series_name = "EnigmaIQ Trivias"
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
        elif mode == "trivias":
            focus_areas = trivia_constants.FOCUS_AREAS_TRIVIAS
        else:
            focus_areas = [
                # 🧠 PSICOLOGÍA Y COMPORTAMIENTO HUMANO
                "SESGOS COGNITIVOS Y TRAMPAS MENTALES: Cómo tu propio cerebro te engaña a diario sin que lo notes. Efecto Dunning-Kruger, sesgo de confirmación, paradoja de la elección.",
                "POR QUÉ HACES LO QUE HACES: Los secretos de la psicología conductual que explican tus compulsiones, miedos irracionales y malas decisiones.",
                "EL PODER OCULTO DE TU INCONSCIENTE: Cómo decisiones que crees tuyas están siendo manipuladas por tu entorno, colores, música y palabras.",
                "MANIPULACIÓN PSICOLÓGICA: Técnicas reales de persuasión que usan empresas, gobiernos y publicidad para controlar tus decisiones.",
                "TRASTORNOS CEREBRALES ALUCINANTES: Casos reales de personas con condiciones cerebrales extrañas como no reconocer caras, sentir que todo es falso o no sentir dolor.",
                # 🧬 EL CUERPO HUMANO
                "SECRETOS DE TU CUERPO QUE NADIE TE CONTÓ: Datos fascinantes sobre cómo funciona tu organismo sin que te des cuenta. El poder del sistema inmune, la regeneración celular.",
                "SUPERPODERES OCULTOS DEL CUERPO HUMANO: La asombrosa capacidad de regeneración del hígado, cómo el corazón crea su propio campo eléctrico o por qué bostezamos en contagio.",
                "LO QUE LA CIENCIA AÚN NO ENTIENDE DEL CUERPO: Misterios médicos sin resolver como el efecto placebo, la anestesia o por qué soñamos.",
                "LOS LÍMITES EXTREMOS DEL CUERPO HUMANO: Hasta dónde puede aguantar el cuerpo sin dormir, sin comer, en frío extremo o bajo presión. Casos reales de supervivencia.",
                "MICROBIOS QUE CONTROLAN TU MENTE: Cómo las bacterias en tu intestino afectan tu estado de ánimo, tus decisiones e incluso tu personalidad.",
                # 🐾 MUNDO ANIMAL
                "SUPERPODERES ANIMALES QUE PARECEN FICCIÓN: Criaturas con capacidades que desafían la lógica. Animales que brillan, regeneran partes del cuerpo o ven lo invisible.",
                "LAS ESTRATEGIAS MÁS BRUTALES DE SUPERVIVENCIA ANIMAL: Engaños, mimetismo, sacrificios y tácticas extremas en el reino animal.",
                "ANIMALES CON COMPORTAMIENTOS HUMANOS: Criaturas que usan herramientas, hacen duelo por sus muertos, comercian, tienen guerras o esclavizan a otras especies.",
                "DEPREDADORES SUBESTIMADOS: Los animales más letales que no parecen peligrosos pero lo son. El animal más mortal del mundo te sorprenderá.",
                "MISTERIOS DEL COMPORTAMIENTO ANIMAL: Comportamientos que la ciencia no puede explicar. Migraciones imposibles, suicidios colectivos o comunicación interestelar.",
                # 🌍 NATURALEZA Y FENÓMENOS NATURALES
                "FENÓMENOS NATURALES QUE PARECEN MAGIA: Relámpagos volcánicos, agujeros azules, glaciares sangrantes, nubes que parecen ovnis y lagos que explotan.",
                "LOS LUGARES MÁS EXTREMOS E INHÓSPITOS DEL PLANETA: Puntos donde la vida parece imposible pero existe. Desiertos helados, profundidades oceánicas, volcanes activos.",
                "MISTERIOS GEOGRÁFICOS QUE LA CIENCIA NO EXPLICA: Límites que la naturaleza impone de formas extrañas. Fronteras invisibles, ecosistemas aislados, anomalías magnéticas.",
                "PLANTAS Y HONGOS CON PODERES OCULTOS: Especies con habilidades increíbles. Redes subterráneas de comunicación, hongos que controlan mentes, plantas carnívoras sorprendentes.",
                "DESASTRES NATURALES QUE CAMBIARON LA HISTORIA: Eventos catastróficos que moldearon civilizaciones enteras y de los que casi nadie habla.",
                # 🔬 CIENCIA Y TECNOLOGÍA
                "INVENTOS ACCIDENTALES QUE CAMBIARON EL MUNDO: Descubrimientos científicos que ocurrieron por error. Microondas, penicilina, rayos X, post-it, Viagra.",
                "TECNOLOGÍA QUE PARECE MAGIA NEGRA: Innovaciones actuales tan avanzadas que suenan a ciencia ficción. Edición genética, computación cuántica, interfaces cerebro-máquina.",
                "LO QUE LA CIENCIA SABE PERO NO TE CUENTA: Descubrimientos científicos reales que suenan a conspiración o son demasiado perturbadores para el público general.",
                "PARADOJAS CIENTÍFICAS QUE TE ROMPERÁN LA CABEZA: Paradojas de la física, el tiempo y la lógica que desafían todo lo que crees saber.",
                "EL LADO OSCURO DE LA TECNOLOGÍA: Cómo funciona realmente internet, la deep web, vigilancia masiva, algoritmos que te conocen mejor que tú mismo.",
                # 🍔 ALIMENTACIÓN Y COCINA
                "LA CIENCIA DETRÁS DE TUS COMIDAS FAVORITAS: Por qué el queso hace agujeros, qué hace que la pizza sea adictiva o por qué la comida sabe diferente en el avión.",
                "ALIMENTOS QUE FUNCIONAN COMO DROGAS: Ciertos alimentos activan los mismos receptores cerebrales que las drogas. Adicción al azúcar, umami, capsaicina y el picante.",
                "LA HISTORIA OCULTA DE LOS ALIMENTOS: El origen sorprendente de lo que comes cada día. Cómo se inventaron los cereales, las patatas fritas, el café instantáneo.",
                "MITOS ALIMENTICIOS QUE LA CIENCIA DESMINTIÓ: Creencias populares sobre comida que son completamente falsas. El mito de las 8 horas de sueño, las 5 comidas al día.",
                "COMIDAS TAN EXTREMAS QUE POCOS SE ATREVEN A PROBAR: Platos de todo el mundo que desafían el estómago y la mente. Delicatessen peligrosas, ingredientes prohibidos.",
                # 🔎 MISTERIOS MODERNOS SIN RESOLVER
                "CASOS SIN RESOLVER QUE DESAFÍAN LA LÓGICA: Desapariciones inexplicables, crímenes perfectos, misterios que la policía no pudo resolver y siguen abiertos.",
                "EXPEDIENTES DESCLASIFICADOS: Secretos de gobierno que salieron a la luz después de décadas. Programas ocultos, experimentos, avistamientos.",
                "FENÓMENOS EXTRAÑOS QUE LA CIENCIA NO PUEDE EXPLICAR: Eventos documentados pero sin explicación científica. Luces fantasmas, sonidos del cielo, lluvias de animales.",
                "HISTORIAS DE GENTE QUE DESAPARECIÓ SIN DEJAR RASTRO: Casos reales de desapariciones misteriosas donde no hubo crimen, solo silencio absoluto.",
                "MENSAJES Y CÓDIGOS QUE NADIE HA PODIDO DESCIFRAR: Manuscritos antiguos, códigos imposibles, mensajes cifrados que han resistido siglos de intentos.",
                # 💪 HISTORIAS DE SUPERVIVENCIA Y SUPERACIÓN
                "HISTORIAS REALES DE SUPERVIVENCIA EXTREMA: Personas que sobrevivieron a situaciones imposibles. Perdidos en el mar, atrapados en montañas, abandonados en la nada.",
                "CASOS DE RESILIENCIA HUMANA QUE PAREN FICCIÓN: Personas que superaron condiciones brutales y salieron adelante contra todo pronóstico.",
                "LOS ERRORES HUMANOS MÁS COSTOSOS DE LA HISTORIA: Errores simples que tuvieron consecuencias catastróficas. Un clic, una palabra, una decisión que cambió todo.",
                "ACTOS DE HEROÍSMO ANÓNIMO QUE SALVARON MILES DE VIDA: Personas comunes que hicieron algo extraordinario sin buscar reconocimiento.",
                "FRAUDES Y ESTAFAS QUE ENGAÑARON A TODO EL MUNDO: Los timos más grandes de la historia. Gente que vendió la Torre Eiffel, islas falsas, engaños que duraron décadas.",
                # 💡 CURIOSIDADES DE LA VIDA COTIDIANA
                "EL ORIGEN SECRETO DE LAS COSAS COTIDIANAS: Cómo se inventaron objetos que usas a diario. El tenedor, el papel higiénico, el cepillo de dientes. Historias bizarras.",
                "DATOS QUE CAMBIARÁN CÓMO VES EL MUNDO: Hechos tan sorprendentes sobre la vida diaria que después de saberlos no podrás dejar de pensarlos.",
                "EL DINERO Y SUS SECRETOS MÁS OSCUROS: Cómo se crea el dinero, por qué inflación, el origen de la deuda, el sistema bancario explicado sin rodeos.",
                "LEYENDAS URBANAS QUE RESULTARON SER CIERTAS: Mitos populares que todos creían falsos pero que realmente ocurrieron. Historias que suenan a mentira pero son verdad.",
                "EL PODER DEL AZAR Y LA PROBABILIDAD EN TU VIDA: Coincidencias imposibles, estadísticas alucinantes, la lotería genética y cómo el azar define tu destino.",
                # 🏆 RÉCORDS Y EXTREMOS
                "RÉCORDS HUMANOS TAN EXTREMOS QUE PAREN MENTIRA: Las marcas más insólitas jamás registradas. Resistencia, fuerza, velocidad, memoria.",
                "CASOS EXTREMOS DE LA NATURALEZA HUMANA: Personas con condiciones, habilidades o historias de vida tan extremas que parecen sacadas de una película.",
                "LOS MAYORES EXPERTOS DEL MUNDO EN COCOSAS: Personas que dedicaron su vida a dominar habilidades absurdas o extremadamente específicas.",
                "OBJETOS Y LUGARES CON RÉCORDS IMPOSIBLES: La cosa más cara, más grande, más pequeña, más antigua, más rara del planeta.",
                # 🌌 EL ESPACIO Y EL UNIVERSO
                "DATOS DEL UNIVERSO QUE TE HARÁN SENTIR INMENSO: Curiosidades sobre el cosmos, agujeros negros, planetas imposibles y el tamaño inimaginable del universo.",
                "LO QUE LA NASA OCULTA SOBRE EL ESPACIO: Datos sorprendentes y poco conocidos sobre las misiones espaciales, la vida en órbita y lo que hay más allá.",
                "EL LADO ATERRADOR DEL ESPACIO: Fenómenos cósmicos que son tan violentos o extraños que cuesta creer que existan. Cuásares, púlsares, estrellas de neutrones.",
                "LA BÚSQUEDA DE VIDA EXTRATERRESTRE: Lo que realmente se sabe sobre ovnis, señales del espacio, planetas habitables y la ecuación de Drake.",
                # 🎨 LENGUAJE, ARTE Y CULTURA
                "CURIOSIDADES DEL LENGUAJE QUE TE SORPRENDERÁN: Palabras intraducibles, idiomas que se extinguen, el origen de las palabras que usas todos los días.",
                "HISTORIAS DETRÁS DE OBRAS DE ARTE FAMOSAS: Secretos y anécdotas ocultas en pinturas, canciones, películas y libros que conoces pero no sabías su trasfondo.",
                "EL SIGNIFICADO OCULTO DETRÁS DE SÍMBOLOS COTIDIANOS: El verdadero origen y significado de símbolos que ves a diario. Marca registrada, play, corazón, símbolos religiosos.",
                "CANCIONES CON HISTORIAS PERTURBADORAS: Hits famosos que esconden tragedias, crímenes o mensajes ocultos que cambiaron la vida de sus creadores.",
                # 💻 INTERNET Y MUNDO DIGITAL
                "LOS SECRETOS DE INTERNET QUE POCOS CONOCEN: Cómo funciona realmente la red, el lado oscuro de los algoritmos, quién controla lo que ves.",
                "HISTORIAS DE HACKERS Y CIBERCRÍMENES ALUCINANTES: Los ataques más increíbles de la historia, robos digitales imposibles, cómo se protege la información.",
                "EL NEGOCIO OCULTO DE TUS DATOS PERSONALES: Cómo las empresas ganan dinero con tu información, qué saben de ti y cómo usarlo a tu favor.",
                "FENÓMENOS VIRALES QUE NADIE ESPERABA: Memes, trends y fenómenos de internet que explotaron sin razón aparente y cambiaron la cultura digital.",
                # 🧩 GENÉTICA Y EVOLUCIÓN
                "CURIOSIDADES DE TU ADN QUE NO SABÍAS: Datos fascinantes sobre tu código genético. Cuánto compartes con un plátano, qué genes heredaste de Neandertal, ADN basura.",
                "LA EVOLUCIÓN EN ACCIÓN: Ejemplos de evolución que están ocurriendo AHORA MISMO en animales y humanos. Adaptaciones rápidas, mutaciones sorprendentes.",
                "LO QUE LA GENÉTICA PUEDE HACER HOY: Edición genética CRISPR, bebés de diseño, resucitar especies extintas. La ciencia ficción ya es realidad.",
                "ENFERMEDADES GENÉTICAS RARAS: Condiciones médicas tan extrañas que afectan a un puñado de personas en el mundo. Casos documentados fascinantes.",
                # 🏛️ CIVILIZACIONES (ocasional, no dominante)
                "DATOS POCO CONOCIDOS DE CIVILIZACIONES ANTIGUAS: Una curiosidad específica y poco conocida de alguna civilización antigua que NO se haya tratado antes.",
            ]
        selected_area = random.choice(focus_areas)
        Messenger.info(f"🎯 Random Focus Area: {selected_area}")

        avoid_msg = ""
        banned_words = "Pobre, Rico, Mentalidad, Escasez, Abundancia, Mindset, Millonario"
        
        combined_avoid = list(titles_to_avoid)
        if extra_avoid:
            # extra_avoid already comes as a formatted string from get_recent_topics
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
        elif mode == "trivias":
            styles = [
                "Base Style: High-contrast professional quiz show studio. Rich dark background with sleek neon teal and emerald green accents, dynamic theatrical down-lighting.",
                "Base Style: Neon Cyberpunk Arcade. Dark obsidian background with glowing neon green and white tactical chalk lines, futuristic holographic displays, and micro-grid patterns.",
                "Base Style: Elegant Minimalist Glassmorphism. Deep dark navy backdrop with frosted glass card placeholders, premium gold/amber glowing edges, and modern clean typography.",
                "Base Style: Cinematic Documentary Trivia. Textured dark slate background, professional cinematic lighting, rich realistic textures (old parchment, magnifying glass, antique maps) in soft focus."
            ]
        else:
            styles = [
                "Base Estilo: Hyper-realistic cinematic lighting. Dark moody colors, misty background, high detail, professional photography style.",
                "Base Estilo: Cinematic National Geographic style documentary. Vibrant colors, ultra-detailed, mysterious and awe-inspiring atmosphere.",
                "Base Estilo: Vintage anatomical/technical sketch on aged parchment. Sepia ink, detailed, mysterious journal look.",
                "Base Estilo: Dark digital art. Neon accents, glitchy textures, high contrast, futuristic mystery vibe.",
                "Base Estilo: Surreal fantasy realism. Luminous ethereal particles, deep cosmic purples and magentas, magical atmosphere, rich volumetric glows."
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
        
        if mode == "trivias":
            full_script_prompt = (
                script_prompt + 
                f"\n\nIDEA A DESARROLLAR: {idea_data.title}\n"
                f"**ESTILOS VISUALES RECOMENDADOS:** {selected_style}\n"
            )
        else:
            full_script_prompt = (
                script_prompt + 
                f"\n\nIDEA A DESARROLLAR: {idea_data.title}\n"
                f"**ESTILOS VISUALES RECOMENDADOS PARA IMÁGENES/MAPAS:** {selected_style}\n"
            )
        if mode == "geography":
            script_schema = GeographyHandler
        elif mode == "trivias":
            script_schema = TriviasHandler
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
