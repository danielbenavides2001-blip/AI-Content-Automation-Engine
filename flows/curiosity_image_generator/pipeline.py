import os
import random
from pathlib import Path
import time
import urllib.request
import pandas as pd
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from tools.common.messenger import Messenger
from tools.text_generation.gemini import GeminiTextGenerator
from tools.image_generation.vertex_ai import VertexAIImageGenerator
from tools.social_media.facebook import FacebookTool
from tools.image_generation.story_card_engine import StoryCardEngine
from typing import Optional
from flows.curiosity_image_generator.models import CuriosityPost
from tools.common.topic_validator import TopicValidator


class CuriosityPipeline:
    def __init__(self) -> None:
        load_dotenv()
        
        # Read settings from environment
        self.project_id = os.getenv("GCP_PROJECT_ID", "facebookbot-502117")
        self.location = os.getenv("GCP_LOCATION", "us-central1")
        self.page_id = os.getenv("FACEBOOK_PAGE_ID")
        self.access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
        
        # Output directories
        self.output_dir = Path(__file__).parent / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.resource_dir = Path(__file__).parent / "resources"
        self.resource_dir.mkdir(parents=True, exist_ok=True)
        
        # History CSV
        self.history_csv = Path(__file__).parent / "curiosity_history.csv"
        if not self.history_csv.exists():
            df = pd.DataFrame(columns=["timestamp", "title", "headline"])
            df.to_csv(self.history_csv, index=False)
            Messenger.info("📊 Initialized new curiosity history tracker.")
        
        # Tools initialization
        self.text_gen = GeminiTextGenerator()
        
        # Initialize Vertex Image Generator (using 3:4 aspect ratio, then we crop to 4:5)
        # Only initialize if Vertex AI is enabled and a project is configured
        use_vertex = os.getenv("USE_VERTEX_AI_IMAGE", "false").lower() == "true"
        if use_vertex and self.project_id:
            self.image_gen = VertexAIImageGenerator(
                project_id=self.project_id,
                location=self.location,
                aspect_ratio="3:4"
            )
        else:
            self.image_gen = None
            Messenger.warning("⚠️  Vertex AI Image generation is DISABLED (USE_VERTEX_AI_IMAGE=false or GCP_PROJECT_ID not set).")
        
        if self.page_id and self.access_token:
            self.fb_tool = FacebookTool(
                page_id=self.page_id,
                access_token=self.access_token
            )
        else:
            self.fb_tool = None
            Messenger.warning("⚠️ Facebook credentials missing in .env. Publishing will not be available.")

    def download_fonts(self) -> tuple[Path, Path]:
        font_dir = self.resource_dir / "fonts"
        font_dir.mkdir(parents=True, exist_ok=True)
        
        font_bold = font_dir / "Montserrat-Bold.ttf"
        font_medium = font_dir / "Montserrat-Medium.ttf"
        
        url_bold = "https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-Bold.ttf"
        url_medium = "https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-Medium.ttf"
        
        if not font_bold.exists():
            try:
                Messenger.info(f"Downloading premium font: {font_bold.name}...")
                urllib.request.urlretrieve(url_bold, font_bold)
            except Exception as e:
                Messenger.warning(f"Could not download bold font: {e}")
                
        if not font_medium.exists():
            try:
                Messenger.info(f"Downloading premium font: {font_medium.name}...")
                urllib.request.urlretrieve(url_medium, font_medium)
            except Exception as e:
                Messenger.warning(f"Could not download medium font: {e}")
                
        return font_bold, font_medium

    def compose_card(self, original_img_path: Path, output_path: Path, headline: str) -> None:
        """
        Composes a highly professional, stunning vertical Curiosity card (1080x1350)
        featuring the generated image, a translucent dark footer, EnigmaIQ branding,
        and centered wrapped text with keyword color highlights.
        """
        Messenger.info("🎨 Composing branded graphic card using Pillow...")
        
        # 1. Setup fonts
        font_bold_path, font_medium_path = self.download_fonts()
        
        try:
            font_title = ImageFont.truetype(str(font_bold_path), 50) # Big bold headline
            font_brand = ImageFont.truetype(str(font_bold_path), 28) # EnigmaIQ name
            font_logo = ImageFont.truetype(str(font_bold_path), 32) # Logo letter
        except Exception:
            font_title = ImageFont.load_default()
            font_brand = ImageFont.load_default()
            font_logo = ImageFont.load_default()
            Messenger.warning("Using fallback default fonts for composition.")

        # 2. Setup canvas
        canvas_w, canvas_h = 1080, 1350
        
        if not original_img_path.exists():
            raise FileNotFoundError(f"Source image not found: {original_img_path}")
            
        orig_img = Image.open(original_img_path).convert("RGBA")
        
        # Smart crop: resize the 3:4 original image to width 1080 (height becomes 1440)
        # then crop the top 1350 pixels so the key elements (at the top) are preserved.
        w_orig, h_orig = orig_img.size
        scale_factor = canvas_w / w_orig
        new_h = int(h_orig * scale_factor)
        resized_img = orig_img.resize((canvas_w, new_h), Image.Resampling.LANCZOS)
        
        # Crop to 1080x1350 from top
        canvas = resized_img.crop((0, 0, canvas_w, canvas_h))
        
        # 3. Create draw context
        overlay = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        
        # Draw dark gradient/overlay at the bottom (solid black deep navy gradient from y=750 to y=1350)
        # We draw layers of increasing opacity
        for y in range(720, 1350):
            # Alpha goes from 0 (at y=720) to 240 (at y=900) and stays at 245 to 255
            if y < 900:
                alpha = int((y - 720) / (900 - 720) * 230)
            else:
                alpha = 230
            # Paint a 1px line
            draw_overlay.line([(0, y), (canvas_w, y)], fill=(8, 10, 16, alpha))
            
        canvas = Image.alpha_composite(canvas, overlay)
        draw = ImageDraw.Draw(canvas)
        
        # 4. Draw Logo Mark & Brand Name (EnigmaIQ) at the bottom footer (y = 860)
        footer_start_y = 860
        logo_x = 80
        logo_radius = 28
        logo_center_y = footer_start_y + logo_radius
        
        # Draw double-ring glowing logo circle
        # Outer ring
        draw.ellipse(
            [logo_x - 4, logo_center_y - logo_radius - 4, logo_x + logo_radius*2 + 4, logo_center_y + logo_radius + 4],
            outline=(60, 235, 255, 120),
            width=2
        )
        # Inner circle background
        draw.ellipse(
            [logo_x, logo_center_y - logo_radius, logo_x + logo_radius*2, logo_center_y + logo_radius],
            fill=(10, 15, 25, 255),
            outline=(60, 235, 255, 255),
            width=3
        )
        # Logo letter "E" centered inside the circle
        logo_text = "E"
        try:
            l_bbox = font_logo.getbbox(logo_text)
            l_w = l_bbox[2] - l_bbox[0]
            l_h = l_bbox[3] - l_bbox[1]
            draw.text(
                (logo_x + (logo_radius*2 - l_w)//2, logo_center_y - l_h//2 - 4),
                logo_text,
                font=font_logo,
                fill=(60, 235, 255, 255)
            )
        except Exception:
            pass
            
        # Draw Brand Name "ENIGMAIQ" next to the logo
        brand_name = "ENIGMAIQ"
        brand_x = logo_x + logo_radius*2 + 20
        brand_y = logo_center_y - 18
        draw.text((brand_x, brand_y), brand_name, font=font_brand, fill=(255, 255, 255, 255))
        
        # Draw elegant dotted separator line next to brand name
        line_start_x = brand_x + 180
        line_end_x = canvas_w - 80
        line_y = brand_y + 16
        
        # Draw dotted line (segments of 4px)
        for dot_x in range(line_start_x, line_end_x, 12):
            draw.rectangle([dot_x, line_y, dot_x + 5, line_y + 2], fill=(60, 235, 255, 100))

        # 5. Centered Word-by-Word wrapped text layout with Highlight color
        # Parse headline into list of tuples: (text, is_highlighted)
        words_raw = headline.split()
        parsed_words = []
        for w in words_raw:
            if w.startswith("[") and w.endswith("]"):
                parsed_words.append((w[1:-1], True))
            elif w.startswith("[") and w.endswith("]."):
                parsed_words.append((w[1:-2] + ".", True))
            elif w.startswith("[") and w.endswith("],"):
                parsed_words.append((w[1:-2] + ",", True))
            else:
                parsed_words.append((w, False))
                
        # Group into lines based on width
        max_line_width = canvas_w - 160 # margins: 80px left and right
        space_width = font_title.getbbox(" ")[2] - font_title.getbbox(" ")[0]
        
        lines = []
        current_line = []
        current_width = 0
        
        for word, is_hl in parsed_words:
            # Measure word
            w_bbox = font_title.getbbox(word)
            w_width = w_bbox[2] - w_bbox[0]
            
            # If line is not empty, add space
            added_width = w_width + (space_width if current_line else 0)
            
            if current_width + added_width <= max_line_width:
                current_line.append((word, is_hl, w_width))
                current_width += added_width
            else:
                if current_line:
                    lines.append(current_line)
                current_line = [(word, is_hl, w_width)]
                current_width = w_width
                
        if current_line:
            lines.append(current_line)
            
        # Draw each line centered horizontally
        start_y = footer_start_y + 90
        line_spacing = 70
        
        for line_idx, line in enumerate(lines):
            # Calculate total width of this line
            total_w = sum(w[2] for w in line) + space_width * (len(line) - 1)
            line_start_x = (canvas_w - total_w) // 2
            
            current_x = line_start_x
            line_y = start_y + (line_idx * line_spacing)
            
            for word, is_hl, w_width in line:
                # Select color: neon cian for highlighted, white for normal
                text_color = (60, 235, 255, 255) if is_hl else (255, 255, 255, 255)
                
                # Draw subtle drop shadow for maximum contrast
                draw.text((current_x + 2, line_y + 2), word, font=font_title, fill=(0, 0, 0, 180))
                # Draw main text
                draw.text((current_x, line_y), word, font=font_title, fill=text_color)
                
                current_x += w_width + space_width
                
        # 6. Save final JPEG image
        final_canvas = canvas.convert("RGB")
        final_canvas.save(output_path, "JPEG", quality=95)
        Messenger.success(f"🎨 Stylized branded card created at: {output_path}")

    def get_past_topics(self) -> list[str]:
        """
        Unifies topic history from curiosity_history.csv, ideas_tracking.csv,
        and automated_posts_history.csv to ensure global zero repetition.
        Preserves chronological order and filters unsafe keywords.
        """
        curiosity_topics = []
        other_topics = []
        
        # 1. Read curiosity_history.csv (PRIORITY 1: 100% preserved)
        if self.history_csv.exists():
            try:
                df = pd.read_csv(self.history_csv)
                if not df.empty and "title" in df.columns:
                    curiosity_topics.extend(df["title"].dropna().tolist())
            except Exception as e:
                Messenger.warning(f"⚠️ Could not read curiosity_history.csv: {e}")

        # 2. Read ideas_tracking.csv
        ideas_csv = Path(__file__).resolve().parent.parent / "image_content_generator" / "out_short" / "ideas_tracking.csv"
        if ideas_csv.exists():
            try:
                df_ideas = pd.read_csv(ideas_csv)
                if not df_ideas.empty and "title" in df_ideas.columns:
                    other_topics.extend(df_ideas["title"].dropna().tolist())
            except Exception as e:
                Messenger.warning(f"⚠️ Could not read ideas_tracking.csv: {e}")

        # 3. Read automated_posts_history.csv
        auto_csv = Path(__file__).resolve().parent.parent / "image_content_generator" / "out_short" / "automated_posts_history.csv"
        if auto_csv.exists():
            try:
                df_auto = pd.read_csv(auto_csv)
                if not df_auto.empty and "topic" in df_auto.columns:
                    other_topics.extend(df_auto["topic"].dropna().tolist())
            except Exception as e:
                Messenger.warning(f"⚠️ Could not read automated_posts_history.csv: {e}")

        # Clean and deduplicate both sets
        clean_curio = TopicValidator.clean_past_titles(curiosity_topics)
        clean_others = TopicValidator.clean_past_titles(other_topics)
        
        # Merge: All curiosity history + unique video topics
        return list(dict.fromkeys(clean_curio + clean_others))

    def run(self, publish: bool = False) -> None:
        Messenger.info("✨ Starting Curiosity Photo Post Pipeline...")
        
        # 1. Ultra-diverse Focus Areas for Global Curiosities (60+ Distinct Domains)
        focus_areas = [
            # REINO ANIMAL Y BIOLOGÍA EXTRAÑA
            "ADAPTACIONES DEPREDADORAS INSÓLITAS: Estrategias de caza asombrosas y poco conocidas (hormigas mandíbula trampa, peces arquero disparando agua, avispa joya zombificadora).",
            "CRIATURAS EXTREMÓFILAS Y RESISTENCIA IMPOSIBLE: Organismos que viven en condiciones extremas de radiación, frío polar, acidez o presión en fuentes termales (Deinococcus radiodurans, gusanos pompeya).",
            "BIOLUMINISCENCIA Y COMUNICACIÓN ÓPTICA: Especies que generan su propia luz en bosques o profundidades para cazar o comunicarse (hongos fantasma, calamar luciérnaga, escarabajos de fuego).",
            "CAMUFLAJES ACTIVOS Y MIMETISMO IMPOSIBLE: Animales que transforman su textura, color y forma en segundos (pulpo mimo, mantis orquídea, insectos corteza de la selva).",
            "REGENERACIÓN CELULAR Y LONGEVIDAD EXTREMA: Animales que desafían el envejecimiento o regeneran órganos completos (tiburón de Groenlandia, medusa inmortal Turritopsis dohrnii, salamandras de cueva olm).",
            "COMUNICACIÓN ANIMAL Y BIOACÚSTICA ALUCINANTE: Especies con sistemas acústicos complejos (pájaros lira imitando sonidos humanos y mecánicos, cantos infrasónicos de ballenas azules, chasquidos de cachalotes).",
            "VENENOS Y BIOQUÍMICA NATURAL: Toxinas y compuestos bioquímicos fascinantes (pez piedra, caracol cono con neurotoxinas ultraprecisas, rana dardo dorada).",
            "SIMBIOSIS ASOMBROSAS DEL REINO ANIMAL: Mutualismos extraños donde especies completamente distintas cooperan para sobrevivir (peces limpiadores, camarones ciegos y gobios vigilantes, tejones mieleros y pájaros guía).",
            "SENTIDOS SOBRENATURALES DE ANIMALES: Animales con magnetorrecepción, electrodetección o visión ultravioleta/infrarroja (ornitorrincos, víboras de foseta, tiburones martillo con ampollas de Lorenzini).",
            "INGENIERÍA ANIMAL Y ARQUITECTURA BIOLÓGICA: Nidos, colmenas y estructuras colosales creadas por animales (termitas con climatización pasiva, pájaros tejedores republicanos, diques de castores visibles desde el espacio).",

            # OCÉANOS Y ABISMOS MARINOS
            "ZONA HADAL Y FOSAS OCEÁNICAS: Criaturas y secretos del abismo bajo 8000 metros de profundidad (Fosa de las Marianas, pez baboso de las Marianas, anfípodos gigantes).",
            "GIGANTISMO ABISAL: El fenómeno de por qué las criaturas de las profundidades marinas crecen a tamaños colosales (isópodos gigantes, cangrejo araña japonés, anfípodos monstruosos).",
            "ECOSISTEMAS DE FUMAROLAS HIDROTERMALES: Vida que no depende de la luz solar sino de azufre y quimiosíntesis a 400°C en grietas volcánicas submarinas.",
            "ANOMALÍAS SUBMARINAS Y RUIDOS INEXPLICABLES: Sonidos de muy baja frecuencia detectados en los océanos del mundo (el 'Bloop', 'Julia', 'Train') y corrientes oceánicas invisibles.",
            "LAGOS Y RÍOS BAJO EL AGUA: Fenómenos de salmuera densa en el lecho marino del Golfo de México donde se forman auténticos lagos y costas submarinas.",

            # PREHISTORIA, PALEONTOLOGÍA Y EVOLUCIÓN
            "ARTRÓPODOS GIGANTES DEL CARBONÍFERO: La época en que el oxígeno abundante creó insectos y miriápodos gigantescos (Meganeura del tamaño de águilas, Arthropleura milpiés de 2 metros).",
            "FAUNA FANTÁSTICA DEL CÁMBRICO: Los primeros animales complejos con anatomías alienígenas en los esquistos de Burgess (Opabinia con 5 ojos, Anomalocaris, Hallucigenia).",
            "MAMÍFEROS GIGANTES DEL PLEISTOCENO: Megafauna colosal olvidada (Glyptodon del tamaño de un automóvil, Megatherium perezoso terrestre gigante de 6 metros, Smilodon populator).",
            "DEPREDADORES MARINOS DEL MESOZOICO: Reptiles marinos prehistóricos aterradores (Mosasaurio de 15 metros, Liopleurodon, Kronosaurus, Shonisaurus).",
            "DINOSAURIOS CON PLUMAS Y COLORACIÓN REAL: Descubrimientos fósiles recientes que revelan el verdadero plumaje, patrones de color y sonidos de los terópodos.",
            "PLANTAS Y BOSQUES PREHISTÓRICOS PERDIDOS: Fósiles de Prototaxites (hongos gigantes de 8 metros que dominaban la tierra antes de los árboles) y selvas fósiles de la Antártida.",
            "AVES COLOSALES PREHISTÓRICAS: Aves gigantes que surcaban los cielos prehistóricos (Argentavis magnificens con 7 metros de envergadura, Pelagornis sandersi).",

            # ARQUEOLOGÍA, MONUMENTOS Y CIUDADES PERDIDAS
            "ARQUITECTURA SUBTERRÁNEA MILENARIA: Ciudades excavadas en roca volcánica de múltiples niveles bajo tierra (Derinkuyu, Kaymakli, iglesias monolíticas de Lalibela).",
            "TEMPLOS MONOLÍTICOS ESCULPIDOS DE UNA SOLA PIEZA: Hazañas de cantería ancestral imposible (el Templo Kailasa en Ellora esculpido de arriba hacia abajo en una sola roca de basalto).",
            "ESTRUCTURAS MEGALÍTICAS DEL NEOLÍTICO: Sitios anteriores a las pirámides con relieves de animales (Karahan Tepe, alineaciones megalíticas de Carnac).",
            "CIUDADES FLOTANTES Y VENECIAS ANCESTRALES: Ciudades antiguas construidas sobre arrecifes de coral en el océano (Nan Madol en Micronesia, canales olvidados de América).",
            "TECNOLOGÍA HIDRÁULICA Y ACUEDUCTOS ANCESTRALES: Sistemas de irrigación y distribución de agua milenarios (qanats persas en el desierto, cisternas romanas de Yerebatan en Estambul).",
            "MISTERIOS DE MESOPOTAMIA Y SUMERIA: Tablillas cuneiformes que relatan listas de reyes antediluvianos, la biblioteca de Asurbanipal y zigurats de ladrillo cocido.",
            "FORTALEZAS Y MUROS CICLÓPEOS: Construcciones con bloques de cientos de toneladas encajados milimétricamente sin mortero (Sacsayhuamán, Ollantaytambo, Baalbek).",
            "GEOGLIFOS Y ARTE RUPESTRE GIGANTESCO: Líneas y figuras en el suelo visibles solo desde el cielo en desiertos del mundo (geoglifos de Nazca, el Gigante de Atacama, hombres de Marree).",

            # RELIQUIAS, OOPARTS Y ARTEFACTOS HISTÓRICOS
            "MANUSCRITOS INDESCIFRABLES Y CÓDICES SECRETOS: Libros antiguos escritos en alfabetos desconocidos con ilustraciones de plantas inexistentes (Manuscrito Voynich, Códice Rohonc).",
            "ALEACIONES Y METALURGIA ANCESTRAL DESCONOCIDA: Materiales con propiedades nanotecnológicas antiguas (el Acero de Damasco con nanotubos de carbono, el Pilar de Hierro de Delhi que no se oxida).",
            "VIDRIO DICROICO Y NANOQUÍMICA ROMANA: Artefactos con partículas de oro y plata que cambian de color con la luz (la Copa de Licurgo del siglo IV).",
            "DISPOSITIVOS ASTRONÓMICOS Y COMPUTADORAS ANTIGUAS: Mecanismos de engranajes y calculadoras celestes de la antigüedad (el Disco Celeste de Nebra de la Edad del Bronce).",
            "CONCRETO ROMANO AUTORREPARABLE: La fórmula milenaria de ceniza volcánica y cal viva que endurece y sella grietas al contacto con el agua marina.",
            "MAPAS HISTÓRICOS CON ENIGMAS GEOGRÁFICOS: Cartografía antigua que representaba costas detalladas antes de su exploración oficial (el Mapa de Piri Reis, mapa de Waldseemüller).",

            # COSMOS, EXOPLANETAS Y ASTRONOMÍA
            "EXOPLANETAS CON CLIMAS Y COMPOSICIÓN EXTREMA: Mundos alienígenas con lluvias de vidrio fundido (HD 189733b), mantos de diamante puro (55 Cancri e), o donde llueve hierro hirviente (WASP-76b).",
            "PLANETAS NÓMADAS INTERESTELARES: Planetas solitarios expulsados de sus sistemas solares que vagan en la oscuridad absoluta de la Vía Láctea sin estrella madre.",
            "CAMPOS MAGNÉTICOS EXTREMOS Y MAGNETARES: Estrellas de neutrones con campos magnéticos tan potentes que disolverían los átomos de un cuerpo a miles de kilómetros.",
            "EL VACÍO DE BOÖTES Y ANOMALÍAS CÓSMICAS: Regiones gigantescas del universo donde casi no existen galaxias ni materia en cientos de millones de años luz.",
            "LUNAS DE HIELO Y OCÉANOS SUBTERRÁNEOS: Océanos de agua líquida bajo cortezas de hielo en el sistema solar (Europa y Ganímedes de Júpiter, Encélado de Saturno con géiseres hidrotermales).",
            "KILONOVAS Y EL ORIGEN DE LOS METALES PRECIOSOS: Colisiones de estrellas de neutrones que forjan y dispersan oro, platino y uranio a través del cosmos.",
            "LA NUBE DE OORT Y LOS CONFINES DEL SISTEMA SOLAR: La gigantesca esfera de billones de cometas de hielo que rodea nuestro sistema solar a un año luz del Sol.",

            # FENÓMENOS TERRESTRES, GEOLOGÍA Y ATMÓSFERA
            "FENÓMENOS ATMOSFÉRICOS ELÉCTRICOS RAROS: Rayos que duran horas continuas o ascienden hacia el espacio (el Relámpago del Catatumbo en Venezuela, espectros rojos 'sprites' y chorros azules en la estratosfera).",
            "PIEDRAS VIAJERAS Y GEOLOGÍA CINÉTICA: Rocas pesadas que se deslizan solas sobre desiertos llanos impulsadas por finas capas de hielo y viento (Racetrack Playa en el Valle de la Muerte).",
            "DUNAS DE ARENA CANTORAS: Desiertos donde el movimiento de las arenas produce un zumbido sonoro de baja frecuencia similar a un órgano musical.",
            "PENITENTES DE HIELO DE GRAN ALTITUD: Agujas afiladas de hielo de varios metros formadas por sublimación solar en los picos más altos de los Andes.",
            "LAGOS QUE CALCIFICAN O CAMBIAN DE COLOR: Lagos hipersalinos con pH extremo que preservan animales como estatuas o tiñen sus aguas de rojo sangre (Lago Natrón en Tanzania).",
            "VOLCANES DE LAVA AZUL Y MINAS DE AZUFRE: Volcanes donde los gases sulfúricos en combustión crean ríos de fuego azul brillante en la noche (Kawah Ijen en Indonesia).",
            "POZOS Y AGUJEROS AZULES PROFUNDOS: Sumideros kársticos verticales en medio de lagunas o arrecifes oceánicos con aguas anóxicas y fósiles intactos (Gran Agujero Azul de Belice, Agujero de Dean).",
            "DESIERTO DE DANAKIL Y LA TIERRA HIRVIENTE: Uno de los lugares más inhóspitos del planeta con piscinas hidrotermales de ácido amarillo fosforescente y volcanes de sal (Depresión de Danakil en Etiopía).",

            # FÍSICA ASOMBROSA, QUÍMICA Y CIENCIA FASCINANTE
            "MATERIALES ULTRA-LIGEROS Y SÓLIDOS IMPOSIBLES: Sustancias creadas por la ciencia con densidades casi nulas y aislamiento térmico brutal (Aerogeles conocidos como 'humo helado').",
            "FLUIDOS NO NEWTONIANOS Y POLÍMEROS VISCOELÁSTICOS: Líquidos que se comportan como sólidos indestructibles ante un impacto rápido y vuelven a líquido en reposo.",
            "SUPERCONDUCTIVIDAD Y LEVITACIÓN CUÁNTICA: Materiales enfriados a temperaturas criogénicas que expulsan líneas de campo magnético y flotan suspendidos en el aire (Efecto Meissner).",
            "FERROFLUIDOS Y MATERIALES MAGNÉTICOS ACTIVOS: Líquidos infundidos con nanopartículas magnéticas que forman agujas y esculturas vivientes ante campos magnéticos.",
            "EXPERIMENTOS CIENTÍFICOS QUE CAMBIARON LA REALIDAD: Descubrimientos de la física sobre cómo la observación altera el comportamiento de las partículas subatómicas.",
            "FÓRMULA Y SECRETOS DEL FUEGO GRIEGO: El arma incendiaria impenetrable del Imperio Bizantino que continuaba ardiendo sobre el agua del mar.",

            # BOTÁNICA INSÓLITA Y HONGOS ASOMBROSOS
            "PLANTAS CARNÍVORAS GIGANTES DE LA SELVA: Plantas con trampas de jarra capaces de capturar y digerir pequeños vertebrados en las selvas de Borneo (Nepenthes rajah).",
            "FLORES MONSTRUOSAS Y CADAVÉRICAS: Especies parásitas sin raíces ni hojas que emiten olores penetrantes y alcanzan tamaños récord (Rafflesia arnoldii, Amorphophallus titanum).",
            "PLANTAS QUE SOBREVIVEN MIL AÑOS CON DOS HOJAS: Especies desérticas fósiles vivientes que absorben agua únicamente de la niebla costera (Welwitschia mirabilis del desierto de Namib).",
            "REDES MICELIALES Y COMUNICACIÓN VEGETAL: El 'Wood Wide Web', redes subterráneas de hongos que conectan árboles de un bosque para compartir nutrientes y alertas químicas.",
            "HONGOS PARÁSITOS Y CONTROL NEUROLÓGICO EN INSECTOS: El mecanismo preciso del hongo Ophiocordyceps que altera el sistema nervioso de hormigas para manipular su comportamiento.",

            # ENIGMAS HUMANOS Y ANOMALÍAS GENÉTICAS
            "ANOMALÍAS GENÉTICAS EXTRAORDINARIAS: Mutaciones reales en el gen LRP5 que otorgan huesos de densidad irrompible, o mutaciones en ACTN3 para fibras musculares de hiper-velocidad.",
            "TETRACROMATISMO Y VISIÓN SOBREHUMANA: La mutación ocular genética presente en algunas personas que les permite percibir 100 millones de tonalidades de color invisibles para la mayoría.",
            "HIPERMNESIA Y MEMORIA AUTOBIOGRÁFICA TOTAL: Personas capaces de recordar con exactitud fotográfica cada segundo, clima y emoción de cualquier día de su vida.",
            "CASOS DE SUPERVIVENCIA EXTREMA CONTRA TODO PRONÓSTICO: Historias médicas reales de reanimaciones tras hipotermia profunda donde el cerebro se preservó sin oxígeno por horas."
        ]

        # Load unified history
        raw_past = self.get_past_topics()
        past_topics = TopicValidator.clean_past_titles(raw_past)
        Messenger.info(f"📚 Loaded {len(past_topics)} unique past topics for anti-repetition protection.")

        # Rejection loop with TopicValidator (up to 5 attempts)
        max_attempts = 5
        post_data: Optional[CuriosityPost] = None
        current_rejection_note = ""

        for attempt in range(1, max_attempts + 1):
            selected_focus = random.choice(focus_areas)
            Messenger.info(f"🎯 [Intento {attempt}/{max_attempts}] Selected Focus Area: {selected_focus[:80]}...")

            avoid_instruction = ""
            if past_topics:
                # Include up to the last 400 topics in the prompt
                avoid_list_str = "\n- ".join(past_topics[-400:])
                avoid_instruction = (
                    "\n\n🚨 **REGLA DE ORO DE NO REPETICIÓN ABSOLUTA:** 🚨\n"
                    "Está ESTRICTAMENTE PROHIBIDO repetir, reutilizar o inspirarte en CUALQUIERA de estos temas ya publicados:\n"
                    f"- {avoid_list_str}\n\n"
                    "Debes elegir un tema, animal, especie, artefacto, lugar o suceso COMPLETAMENTE NUEVO y diferente a la lista anterior."
                )

            prompt = f"""
Eres un redactor e investigador experto para la página "EnigmaIQ" en Facebook.
Tu misión es generar una publicación gráfica y viral de altísimo impacto sobre una curiosidad o descubrimiento fascinante del mundo (animales insólitos, prehistoria, arqueología, espacio, ciencia o misterios del planeta).

**ÁREA DE ENFOQUE OBLIGATORIA:**
{selected_focus}

**REGLAS ESTRICTAS DE CONTENIDO:**
1. 🛡️ **BRAND SAFETY (FACEBOOK):** 100% apto para todo público. Cero gore, cero violencia, cero sangre, cero crueldad.
2. 🌟 **MÁXIMO IMPACTO Y CURIOSIDAD:** Debe ser un hecho 100% real, verificable y asombroso que despierte curiosidad inmediata.
3. 🎯 **COHERENCIA TOTAL:** El `image_prompt`, el `headline`, el `card_fact` y el `caption` deben estar 100% sincronizados y coincidir exactamente con el mismo tema específico.
4. ✍️ **TEXTO ULTRA-CORTO Y PUNCHY (MÁXIMA LEGIBILIDAD):** 
   - `headline`: DEBE ser breve y potente, de ÚNICAMENTE 8 A 12 PALABRAS en mayúsculas, con 2-3 palabras clave envueltas en `[corchetes]`.
   - `card_fact`: Una sola frase breve de 12 a 18 palabras explicando el dato asombroso para mostrar en la imagen.
5. 🎨 **IMAGEN HIPERREALISTA:** El `image_prompt` debe describir el sujeto (animal, fósil, estructura, fenómeno o lugar) con estética cinematográfica de National Geographic / 8k, ubicando el elemento principal en el 60% superior de la imagen (aspect ratio 4:5 vertical) para dejar el 40% inferior libre para el texto.
{avoid_instruction}
{current_rejection_note}
"""
            Messenger.info(f"🧠 Generating curiosity story via Gemini (Attempt {attempt}/{max_attempts})...")
            candidate_post: CuriosityPost = self.text_gen.generate_text(prompt, CuriosityPost)

            # Validate against past topics with TopicValidator
            is_dup, matched_past, reason = TopicValidator.is_duplicate(
                candidate=candidate_post.title,
                past_titles=past_topics,
                headline=candidate_post.headline
            )

            if is_dup:
                Messenger.warning(
                    f"⚠️ [RECHAZO POR DUPLICIDAD - Intento {attempt}/{max_attempts}]:\n"
                    f"   Propuesta descartada: '{candidate_post.title}'\n"
                    f"   Colisiona con tema previo: '{matched_past}'\n"
                    f"   Motivo de rechazo: {reason}\n"
                    f"   Generando nuevo tema distinto..."
                )
                current_rejection_note = (
                    f"\n\n🚨 ERROR CRÍTICO: Tu propuesta anterior '{candidate_post.title}' fue RECHAZADA "
                    f"porque coincide con el tema ya publicado: '{matched_past}' ({reason}). "
                    f"Está TOTALMENTE PROHIBIDO volver a proponer esta entidad, animal, lugar o concepto. "
                    f"Genera OBLIGATORIAMENTE un tema COMPLETAMENTE DISTINTO en otra categoría."
                )
                continue

            # Validated unique topic!
            post_data = candidate_post
            Messenger.success(f"🎉 Tema 100% único y original validado: '{post_data.title}'")
            break

        if post_data is None:
            post_data = candidate_post
            Messenger.warning("⚠️ Se agotaron los intentos de validación; usando última propuesta generada.")

        Messenger.info(f"📌 Topic: {post_data.title}")
        Messenger.info(f"📰 Headline: {post_data.headline}")
        Messenger.info(f"📝 Caption preview:\n{post_data.caption[:150]}...")
        Messenger.info(f"🎨 Image Prompt: {post_data.image_prompt}")
        
        # 2. Generate Background Image via Vertex AI
        timestamp = int(time.time())
        raw_image_path = self.output_dir / f"raw_curiosity_{timestamp}.jpg"
        composed_image_path = self.output_dir / f"curiosity_card_{timestamp}.jpg"
        
        if self.image_gen is None:
            Messenger.error("❌ Cannot generate image: Vertex AI is disabled. Set USE_VERTEX_AI_IMAGE=true and GCP_PROJECT_ID in your environment to enable image generation.")
            raise RuntimeError("Vertex AI Image generation is disabled. Update USE_VERTEX_AI_IMAGE and GCP_PROJECT_ID.")
        
        Messenger.info("🎨 Sending request to Vertex AI (Imagen 3)...")
        try:
            self.image_gen.generate_image(
                prompt=post_data.image_prompt,
                output_path=raw_image_path
            )
        except Exception as e:
            Messenger.error(f"❌ Failed to generate image via Vertex AI: {str(e)}")
            raise e
            
        # 3. Compose styled graphic card selecting randomly between the 5 viral templates
        card_engine = StoryCardEngine()
        card_engine.compose_random_template(
            img_path=raw_image_path,
            output_path=composed_image_path,
            headline=post_data.headline,
            fact_text=post_data.card_fact,
            category=post_data.title[:20],
            is_story=False,
        )
        
        # Clean up temporary raw image
        raw_image_path.unlink(missing_ok=True)
        
        # Save new topic to history
        try:
            new_row = pd.DataFrame([{
                "timestamp": timestamp,
                "title": post_data.title,
                "headline": post_data.headline
            }])
            df_history = pd.read_csv(self.history_csv) if self.history_csv.exists() else pd.DataFrame(columns=["timestamp", "title", "headline"])
            df_history = pd.concat([df_history, new_row], ignore_index=True)
            df_history.to_csv(self.history_csv, index=False)
            Messenger.success(f"💾 Added '{post_data.title}' to curiosity history.")
        except Exception as hist_e:
            Messenger.warning(f"⚠️ Failed to save to history file: {hist_e}")
            
        # 4. Publish to Facebook if requested
        if publish:
            if not self.fb_tool:
                raise ValueError("❌ Cannot publish: Facebook credentials are missing in .env")
                
            Messenger.info("🚀 Publishing photo post to EnigmaIQ Facebook page...")
            try:
                photo_id = self.fb_tool.upload_photo(
                    file_path=composed_image_path,
                    caption=post_data.caption
                )
                Messenger.success(f"🎉 Success! Photo post published to Facebook. ID: {photo_id}")
                
                # 5. Auto-comment to boost early engagement (algorithm signal)
                if photo_id:
                    try:
                        Messenger.info("💬 Generating auto-engagement comment...")
                        comment_prompt = (
                            f'Eres el creador de "EnigmaIQ". Acabas de publicar una imagen sobre: "{post_data.title}".\n'
                            f'Escribe un comentario corto (1 sola línea) en español como una pregunta intrigante '
                            f'que invite a los seguidores a debatir o comentar si ya conocían este misterio, lugar o descubrimiento.\n'
                            f'El tono debe ser curioso, amigable y natural, sin hashtags ni preguntas sobre animales.\n'
                            f'Ejemplo: "¿Sabías de la existencia de este lugar? ¿Te atreverías a visitarlo? 🏛️ Dejen su opinión abajo 👇"'
                        )
                        comment_text = self.text_gen.generate(comment_prompt).strip()
                        self.fb_tool.add_comment(photo_id, comment_text)
                        Messenger.success(f"✅ Auto-comment posted to drive engagement.")
                    except Exception as comment_e:
                        Messenger.warning(f"⚠️ Auto-comment failed (non-fatal): {comment_e}")
                        
            except Exception as e:
                Messenger.error(f"❌ Failed to publish photo post: {str(e)}")
                raise e
        else:
            Messenger.success(f"💾 Dry-run complete. Styled card saved locally at: {composed_image_path}")

