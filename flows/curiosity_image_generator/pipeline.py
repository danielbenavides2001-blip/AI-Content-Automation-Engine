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
from flows.curiosity_image_generator.models import CuriosityPost


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
        raw_topics = []
        
        # 1. Read curiosity_history.csv
        if self.history_csv.exists():
            try:
                df = pd.read_csv(self.history_csv)
                if not df.empty and "title" in df.columns:
                    raw_topics.extend(df["title"].dropna().tolist())
            except Exception as e:
                Messenger.warning(f"⚠️ Could not read curiosity_history.csv: {e}")

        # 2. Read ideas_tracking.csv
        ideas_csv = Path(__file__).resolve().parent.parent / "image_content_generator" / "out_short" / "ideas_tracking.csv"
        if ideas_csv.exists():
            try:
                df_ideas = pd.read_csv(ideas_csv)
                if not df_ideas.empty and "title" in df_ideas.columns:
                    raw_topics.extend(df_ideas["title"].dropna().tolist())
            except Exception as e:
                Messenger.warning(f"⚠️ Could not read ideas_tracking.csv: {e}")

        # 3. Read automated_posts_history.csv
        auto_csv = Path(__file__).resolve().parent.parent / "image_content_generator" / "out_short" / "automated_posts_history.csv"
        if auto_csv.exists():
            try:
                df_auto = pd.read_csv(auto_csv)
                if not df_auto.empty and "topic" in df_auto.columns:
                    raw_topics.extend(df_auto["topic"].dropna().tolist())
            except Exception as e:
                Messenger.warning(f"⚠️ Could not read automated_posts_history.csv: {e}")

        # Deduplicate while preserving chronological order (most recent at the end)
        deduped = list(dict.fromkeys([str(t).strip() for t in raw_topics if str(t).strip() and str(t).strip().lower() != "curiosity image"]))
        
        # Filter out violent/unsafe words for Facebook brand safety
        unsafe_words = ["muerte", "mortal", "masacre", "asesin", "mata", "letal", "tragedia", "destru", "sangre", "gore", "cadáver", "herido", "suicidi", "manson", "infierno", "terror", "violaci"]
        safe_topics = [t for t in deduped if not any(w in str(t).lower() for w in unsafe_words)]
        
        # Keep up to the last 300 topics
        return safe_topics[-300:]

    def run(self, publish: bool = False) -> None:
        Messenger.info("✨ Starting Curiosity Photo Post Pipeline...")
        
        # 1. Diverse Focus Areas for Global Curiosities (ALL TOPICS INCLUDED: Animals, Prehistory, Space, Archaeology, Science, Oceans)
        focus_areas = [
            "REINO ANIMAL INSÓLITO Y ADAPTACIONES EXTREMAS: Animales con habilidades asombrosas, criaturas de las profundidades abisales, camuflajes imposibles, animales bioluminiscentes y récords del reino animal (fuerza, velocidad, longevidad, sentidos).",
            "PREHISTORIA, PALEONTOLOGÍA Y FÓSILES: Criaturas prehistóricas colosales (megalodón, titanoboa, dinosaurios, mamuts lanudos), fósiles asombrosos y misterios de la evolución en la Tierra.",
            "ARQUEOLOGÍA Y CIVILIZACIONES ANTIGUAS: Misterios de civilizaciones perdidas (Egipto, Mayas, Mesopotamia, Sumeria, Grecia antigua), templos ocultos, construcciones megalíticas y tumbas ancestrales.",
            "ENIGMAS HISTÓRICOS Y RELIQUIAS: Artefactos fuera de su tiempo (ooparts), manuscritos indescifrables, mapas antiguos imposibles y tesoros históricos perdidos.",
            "MISTERIOS DEL COSMOS Y ASTRONOMÍA: Descubrimientos espaciales alucinantes, exoplanetas con climas extremos, agujeros negros, señales cósmicas y anomalías del universo.",
            "FENÓMENOS TERRESTRES Y GEOLOGÍA INSÓLITA: Lugares en la Tierra que parecen de otro planeta (el Ojo del Sahara, cuevas de cristales gigantes de Naica, volcanes de lava azul, lagos rosados).",
            "CIENCIA FASCINANTE Y FÍSICA ASOMBROSA: Paradojas cuánticas, experimentos científicos históricos revolucionarios, propiedades extrañas de la materia y descubrimientos que desafían la intuición humana.",
            "INVENTOS Y TECNOLOGÍA ANCESTRAL: Mecanismos de hace miles de años (Mecanismo de Anticitera), arquitectura antisísmica milenaria, el fuego griego, y tecnologías olvidadas de la antigüedad.",
            "OCÉANOS Y ABISMOS MARINOS: Fosas oceánicas inexploradas (Fosa de las Marianas), criaturas de la zona abisal, ciudades sumergidas y anomalías submarinas.",
            "DATOS CURIOSOS GLOBALES Y LUGARES ENIGMÁTICOS: Hechos 100% reales sobre monumentos, lugares prohibidos (Bóveda Global de Semillas de Svalbard, Zona del Silencio), ciudades subterráneas y secretos de nuestro planeta."
        ]
        selected_focus = random.choice(focus_areas)
        Messenger.info(f"🎯 Selected Focus Area: {selected_focus}")

        # Load unified history
        past_topics = self.get_past_topics()
        avoid_instruction = ""
        if past_topics:
            avoid_list_str = "\n- ".join(past_topics)
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
"""
        
        Messenger.info("🧠 Generating curiosity story via Gemini...")
        post_data: CuriosityPost = self.text_gen.generate_text(prompt, CuriosityPost)
        
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

