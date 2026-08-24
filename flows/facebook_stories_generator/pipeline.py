import os
import random
import time
import urllib.request
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from tools.common.messenger import Messenger
from tools.text_generation.gemini import GeminiTextGenerator
from tools.image_generation.vertex_ai import VertexAIImageGenerator
from tools.social_media.facebook import FacebookTool
from tools.image_generation.story_card_engine import StoryCardEngine
from flows.facebook_stories_generator.models import FacebookStoryPost


class FacebookStoryPipeline:
    def __init__(self) -> None:
        load_dotenv()
        
        # Environment settings
        self.project_id = os.getenv("GCP_PROJECT_ID", "facebookbot-502117")
        self.location = os.getenv("GCP_LOCATION", "us-central1")
        self.page_id = os.getenv("FACEBOOK_PAGE_ID")
        self.access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
        
        # Directories
        self.output_dir = Path(__file__).parent / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.resource_dir = Path(__file__).parent / "resources"
        self.resource_dir.mkdir(parents=True, exist_ok=True)
        
        # History CSV
        self.history_csv = Path(__file__).parent / "story_history.csv"
        if not self.history_csv.exists():
            df = pd.DataFrame(columns=["timestamp", "title", "category", "headline"])
            df.to_csv(self.history_csv, index=False)
            Messenger.info("📊 Initialized new Facebook Stories history tracker.")
        
        # Tools
        self.text_gen = GeminiTextGenerator()
        
        use_vertex = os.getenv("USE_VERTEX_AI_IMAGE", "false").lower() == "true"
        if use_vertex and self.project_id:
            self.image_gen = VertexAIImageGenerator(
                project_id=self.project_id,
                location=self.location,
                aspect_ratio="9:16"
            )
        else:
            self.image_gen = None
            Messenger.warning("⚠️ Vertex AI Image generation disabled (USE_VERTEX_AI_IMAGE=false or GCP_PROJECT_ID missing).")
            
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
                Messenger.info(f"Downloading font: {font_bold.name}...")
                urllib.request.urlretrieve(url_bold, font_bold)
            except Exception as e:
                Messenger.warning(f"Could not download font {font_bold.name}: {e}")
                
        if not font_medium.exists():
            try:
                Messenger.info(f"Downloading font: {font_medium.name}...")
                urllib.request.urlretrieve(url_medium, font_medium)
            except Exception as e:
                Messenger.warning(f"Could not download font {font_medium.name}: {e}")
                
        return font_bold, font_medium

    def compose_story_card(self, original_img_path: Path, output_path: Path, post_data: FacebookStoryPost) -> None:
        """
        Composes a high-impact, full-screen vertical 9:16 (1080x1920) Facebook Story card.
        Layout:
        - Top: Category Pill badge + EnigmaIQ branding (below status bar safe area)
        - Middle: Stunning AI generated imagery
        - Bottom: Dark translucent card with bold question + keyword color highlights + concise explanation.
        """
        Messenger.info("🎨 Composing 9:16 full-screen Facebook Story card...")
        
        font_bold_path, font_medium_path = self.download_fonts()
        
        try:
            font_badge = ImageFont.truetype(str(font_bold_path), 26)
            font_brand = ImageFont.truetype(str(font_bold_path), 28)
            font_headline = ImageFont.truetype(str(font_bold_path), 46)
            font_body = ImageFont.truetype(str(font_medium_path), 32)
            font_cta = ImageFont.truetype(str(font_bold_path), 24)
        except Exception:
            font_badge = font_brand = font_headline = font_body = font_cta = ImageFont.load_default()
            Messenger.warning("Using fallback default fonts for story card composition.")
            
        canvas_w, canvas_h = 1080, 1920
        
        if not original_img_path.exists():
            raise FileNotFoundError(f"Source image not found: {original_img_path}")
            
        orig_img = Image.open(original_img_path).convert("RGBA")
        
        # Fit image to 1080x1920 canvas
        w_orig, h_orig = orig_img.size
        scale = max(canvas_w / w_orig, canvas_h / h_orig)
        new_w, new_h = int(w_orig * scale), int(h_orig * scale)
        resized_img = orig_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Center crop to 1080x1920
        crop_left = (new_w - canvas_w) // 2
        crop_top = (new_h - canvas_h) // 2
        canvas = resized_img.crop((crop_left, crop_top, crop_left + canvas_w, crop_top + canvas_h))
        
        # ── 1. Create Dark Gradient Overlay at Bottom (y = 900 to 1920) ────────
        overlay = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        
        for y in range(850, 1920):
            if y < 1150:
                alpha = int((y - 850) / (1150 - 850) * 235)
            else:
                alpha = 245
            draw_overlay.line([(0, y), (canvas_w, y)], fill=(6, 8, 15, alpha))
            
        # Subtle top vignette for header readability
        for y in range(0, 300):
            alpha = int((1 - (y / 300)) * 170)
            draw_overlay.line([(0, y), (canvas_w, y)], fill=(5, 6, 12, alpha))
            
        canvas = Image.alpha_composite(canvas, overlay)
        draw = ImageDraw.Draw(canvas)
        
        # ── 2. Top Header (Safe area: y = 140) ──────────────────────────────────
        top_y = 140
        category_text = f"  {post_data.category_label.upper()}  "
        
        # Measure category badge
        cat_bbox = font_badge.getbbox(category_text)
        cat_w = cat_bbox[2] - cat_bbox[0] + 24
        cat_h = 44
        cat_x = 70
        
        # Draw category pill badge (glowing cyan outline + dark fill)
        draw.rounded_rectangle(
            [cat_x, top_y, cat_x + cat_w, top_y + cat_h],
            radius=12,
            fill=(10, 20, 35, 230),
            outline=(60, 235, 255, 220),
            width=2
        )
        draw.text((cat_x + 12, top_y + 8), category_text.strip(), font=font_badge, fill=(60, 235, 255, 255))
        
        # Draw EnigmaIQ branding on the right
        brand_text = "ENIGMAIQ"
        brand_bbox = font_brand.getbbox(brand_text)
        brand_w = brand_bbox[2] - brand_bbox[0]
        brand_x = canvas_w - 70 - brand_w
        draw.text((brand_x, top_y + 6), brand_text, font=font_brand, fill=(255, 255, 255, 240))
        
        # ── 3. Bottom Content Box (y = 1100 to 1800) ───────────────────────────
        card_x = 55
        card_w = canvas_w - (card_x * 2) # 970px
        card_y = 1120
        card_h = 680
        
        # Draw sleek rounded translucent backing container
        draw.rounded_rectangle(
            [card_x, card_y, card_x + card_w, card_y + card_h],
            radius=28,
            fill=(10, 14, 24, 210),
            outline=(255, 255, 255, 35),
            width=1
        )
        
        # ── 4. Render Headline with Keyword Highlights ─────────────────────────
        words_raw = post_data.headline.split()
        parsed_words = []
        for w in words_raw:
            if w.startswith("[") and w.endswith("]"):
                parsed_words.append((w[1:-1], True))
            elif w.startswith("[") and (w.endswith("],") or w.endswith("]?") or w.endswith("]!")):
                parsed_words.append((w[1:-2] + w[-1], True))
            elif w.startswith("¿[") and w.endswith("]"):
                parsed_words.append(("¿" + w[2:-1], True))
            elif w.startswith("¡[") and w.endswith("]"):
                parsed_words.append(("¡" + w[2:-1], True))
            else:
                parsed_words.append((w, False))
                
        max_text_w = card_w - 80 # 40px margin on each side
        space_w = font_headline.getbbox(" ")[2] - font_headline.getbbox(" ")[0]
        
        headline_lines = []
        curr_line = []
        curr_width = 0
        
        for word, is_hl in parsed_words:
            w_box = font_headline.getbbox(word)
            w_len = w_box[2] - w_box[0]
            add_w = w_len + (space_w if curr_line else 0)
            
            if curr_width + add_w <= max_text_w:
                curr_line.append((word, is_hl, w_len))
                curr_width += add_w
            else:
                if curr_line:
                    headline_lines.append(curr_line)
                curr_line = [(word, is_hl, w_len)]
                curr_width = w_len
        if curr_line:
            headline_lines.append(curr_line)
            
        # Draw headline lines
        head_start_y = card_y + 45
        head_line_spacing = 60
        for idx, line in enumerate(headline_lines):
            line_w = sum(item[2] for item in line) + space_w * (len(line) - 1)
            line_x = card_x + 40
            line_y = head_start_y + (idx * head_line_spacing)
            
            curr_x = line_x
            for word, is_hl, w_len in line:
                color = (60, 235, 255, 255) if is_hl else (255, 255, 255, 255)
                # Drop shadow
                draw.text((curr_x + 2, line_y + 2), word, font=font_headline, fill=(0, 0, 0, 180))
                draw.text((curr_x, line_y), word, font=font_headline, fill=color)
                curr_x += w_len + space_w
                
        # ── 5. Golden Divider Line ─────────────────────────────────────────────
        divider_y = head_start_y + (len(headline_lines) * head_line_spacing) + 18
        draw.line([(card_x + 40, divider_y), (card_x + card_w - 40, divider_y)], fill=(60, 235, 255, 120), width=2)
        
        # ── 6. Render Fact Body Text ───────────────────────────────────────────
        body_words = post_data.fact_text.split()
        body_lines = []
        curr_b_line = []
        curr_b_w = 0
        b_space_w = font_body.getbbox(" ")[2] - font_body.getbbox(" ")[0]
        
        for w in body_words:
            w_box = font_body.getbbox(w)
            w_len = w_box[2] - w_box[0]
            add_w = w_len + (b_space_w if curr_b_line else 0)
            if curr_b_w + add_w <= max_text_w:
                curr_b_line.append(w)
                curr_b_w += add_w
            else:
                if curr_b_line:
                    body_lines.append(" ".join(curr_b_line))
                curr_b_line = [w]
                curr_b_w = w_len
        if curr_b_line:
            body_lines.append(" ".join(curr_b_line))
            
        body_start_y = divider_y + 24
        body_line_spacing = 46
        for idx, line_text in enumerate(body_lines):
            draw.text((card_x + 40, body_start_y + (idx * body_line_spacing)), line_text, font=font_body, fill=(225, 235, 245, 255))
            
        # ── 7. Bottom CTA Footer (Swipe / Tap for Next Story) ──────────────────
        cta_text = "🔥 TOCA LA PANTALLA PARA MÁS HISTORIAS"
        cta_bbox = font_cta.getbbox(cta_text)
        cta_w = cta_bbox[2] - cta_bbox[0]
        cta_x = (canvas_w - cta_w) // 2
        cta_y = card_y + card_h - 60
        
        draw.text((cta_x, cta_y), cta_text, font=font_cta, fill=(255, 235, 60, 240))
        
        # Save final 9:16 story image
        final_canvas = canvas.convert("RGB")
        final_canvas.save(output_path, "JPEG", quality=95)
        Messenger.success(f"🎨 Stylized 9:16 Facebook Story card created at: {output_path}")

    def get_past_topics(self) -> list[str]:
        """
        Unifies topic history from story_history.csv, curiosity_history.csv,
        ideas_tracking.csv, and automated_posts_history.csv to ensure 0 repetition.
        """
        raw_topics = []
        
        # 1. Read story_history.csv
        if self.history_csv.exists():
            try:
                df = pd.read_csv(self.history_csv)
                if not df.empty and "title" in df.columns:
                    raw_topics.extend(df["title"].dropna().tolist())
            except Exception:
                pass

        # 2. Read curiosity_history.csv
        curiosity_csv = Path(__file__).resolve().parent.parent / "curiosity_image_generator" / "curiosity_history.csv"
        if curiosity_csv.exists():
            try:
                df_cur = pd.read_csv(curiosity_csv)
                if not df_cur.empty and "title" in df_cur.columns:
                    raw_topics.extend(df_cur["title"].dropna().tolist())
            except Exception:
                pass

        # 3. Read ideas_tracking.csv
        ideas_csv = Path(__file__).resolve().parent.parent / "image_content_generator" / "out_short" / "ideas_tracking.csv"
        if ideas_csv.exists():
            try:
                df_ideas = pd.read_csv(ideas_csv)
                if not df_ideas.empty and "title" in df_ideas.columns:
                    raw_topics.extend(df_ideas["title"].dropna().tolist())
            except Exception:
                pass

        # 4. Read automated_posts_history.csv
        auto_csv = Path(__file__).resolve().parent.parent / "image_content_generator" / "out_short" / "automated_posts_history.csv"
        if auto_csv.exists():
            try:
                df_auto = pd.read_csv(auto_csv)
                if not df_auto.empty and "topic" in df_auto.columns:
                    raw_topics.extend(df_auto["topic"].dropna().tolist())
            except Exception:
                pass

        # Deduplicate preserving order
        deduped = list(dict.fromkeys([str(t).strip() for t in raw_topics if str(t).strip() and str(t).strip().lower() != "curiosity image"]))
        
        # Filter violent keywords
        unsafe_words = ["muerte", "mortal", "masacre", "asesin", "mata", "letal", "tragedia", "destru", "sangre", "gore", "cadáver", "herido", "suicidi", "manson", "infierno", "terror", "violaci"]
        safe_topics = [t for t in deduped if not any(w in str(t).lower() for w in unsafe_words)]
        
        return safe_topics[-300:]

    def generate_single_story(self, publish: bool = False) -> Path:
        """
        Generates and optionally publishes a single Facebook Story.
        """
        focus_areas = [
            ("ARQUEOLOGÍA Y CIVILIZACIONES", "Misterios de civilizaciones perdidas (Egipto, Mayas, Sumeria, Grecia antigua), templos ocultos, construcciones megalíticas imposibles y tumbas ancestrales."),
            ("MISTERIOS DEL ESPACIO", "Descubrimientos espaciales alucinantes, exoplanetas con climas extremos, estructuras cósmicas gigantescas, señales de radio espaciales y anomalías del universo."),
            ("GEOLOGÍA INSÓLITA", "Lugares en la Tierra que parecen de otro planeta (el Ojo del Sahara, la Puerta al Infierno en Turkmenistán, cuevas de cristales gigantes de Naica, lagos rosados)."),
            ("ENIGMAS HISTÓRICOS", "Artefactos fuera de su tiempo (ooparts), manuscritos indescifrables (como el Manuscrito Voynich), mapas antiguos imposibles y tesoros históricos perdidos."),
            ("CIENCIA ASOMBROSA", "Paradojas de la física cuántica, experimentos científicos revolucionarios, propiedades extrañas de la materia y descubrimientos que desafían la intuición humana."),
            ("TECNOLOGÍA ANCESTRAL", "Mecanismos y computadoras de hace miles de años (Mecanismo de Anticitera), arquitectura antisísmica milenaria, el fuego griego y secretos constructivos perdidos."),
            ("CULTURAS DEL MUNDO", "Ciudades subterráneas (Derinkuyu), rituales y templos sagrados prohibidos, fortalezas inexpugnables y tradiciones milenarias."),
            ("LUGARES SECRETOS", "Hechos 100% reales sobre monumentos, lugares prohibidos (Bóveda Global de Semillas de Svalbard, Zona del Silencio), ciudades fantasma y secretos de nuestro planeta.")
        ]
        
        category_name, category_desc = random.choice(focus_areas)
        Messenger.info(f"\n🌟 Selected Story Focus: {category_name} - {category_desc}")
        
        past_topics = self.get_past_topics()
        avoid_instruction = ""
        if past_topics:
            avoid_list_str = "\n- ".join(past_topics)
            avoid_instruction = (
                "\n\n🚨 **REGLA DE ORO DE NO REPETICIÓN ABSOLUTA:** 🚨\n"
                "Está ESTRICTAMENTE PROHIBIDO repetir o reutilizar CUALQUIERA de estos temas ya publicados:\n"
                f"- {avoid_list_str}\n\n"
                "Debes inventar un tema, lugar, artefacto o suceso COMPLETAMENTE NUEVO."
            )

        banned_words = "animal, animales, pájaro, ave, pez, peces, insecto, insectos, reptil, reptiles, mamífero, mamíferos, fauna, perro, gato, pulpo, delfín, ballena, araña, tarántula, langosta, cangrejo, loro, guacamaya, especie, criatura, biológico, biología, mascota, mascotas"

        prompt = f"""
Eres un redactor y estratega de contenido viral para las HISTORIAS DE FACEBOOK de "EnigmaIQ".
Tu objetivo es crear una HISTORIA VERTICAL (9:16) de altísimo impacto y curiosidad que detenga el scroll instantáneamente.

**CATEGORÍA ASIGNADA:**
{category_name}: {category_desc}

**REGLAS ESTRICTAS DE CONTENIDO:**
1. 🚫 **PROHIBICIÓN TOTAL DE ANIMALES:** Está TERMINANTEMENTE PROHIBIDO generar contenido sobre animales, fauna, biología, insectos o mascotas. Concéntrate 100% en historia, civilizaciones, arqueología, espacio, ciencia, geografía o tecnología.
2. 🚫 **PALABRAS PROHIBIDAS:** {banned_words}
3. 🛡️ **BRAND SAFETY:** 100% apto para todo público. Cero gore, cero violencia, cero sangre, cero tragedias gráficas.
4. 💥 **GANCHO EXPLOSIVO:** `headline` debe ser una pregunta intrigante o afirmación impactante de 8-15 palabras con 2-4 palabras clave envueltas en `[corchetes]`.
5. 📖 **DATO CURIOSO:** `fact_text` debe ser una explicación clara y asombrosa de 25-40 palabras que deje al usuario con la boca abierta.
6. 🎨 **PROMPT VISUAL:** `image_prompt` en inglés para Imagen 3 (9:16 vertical), ultra detallado, cinematográfico, con el sujeto principal en la mitad superior.
{avoid_instruction}
"""
        
        Messenger.info("🧠 Generating story script via Gemini...")
        post_data: FacebookStoryPost = self.text_gen.generate_text(prompt, FacebookStoryPost)
        
        Messenger.info(f"📌 Story Topic: {post_data.title}")
        Messenger.info(f"🏷️ Category: {post_data.category_label}")
        Messenger.info(f"📰 Headline: {post_data.headline}")
        Messenger.info(f"📝 Fact: {post_data.fact_text}")
        Messenger.info(f"🎨 Image Prompt: {post_data.image_prompt}")
        
        timestamp = int(time.time())
        raw_img_path = self.output_dir / f"raw_story_{timestamp}.jpg"
        composed_img_path = self.output_dir / f"story_card_{timestamp}.jpg"
        
        if self.image_gen is None:
            Messenger.error("❌ Vertex AI Image generator is disabled.")
            raise RuntimeError("Vertex AI is disabled. Update USE_VERTEX_AI_IMAGE and GCP_PROJECT_ID.")
            
        Messenger.info("🎨 Generating 9:16 vertical image via Vertex AI (Imagen 3)...")
        try:
            self.image_gen.generate_image(
                prompt=post_data.image_prompt,
                output_path=raw_img_path
            )
        except Exception as e:
            Messenger.error(f"❌ Failed to generate story image: {e}")
            raise e
            
        # 3. Compose 9:16 vertical story selecting randomly between the 5 viral templates
        card_engine = StoryCardEngine()
        card_engine.compose_random_template(
            img_path=raw_img_path,
            output_path=composed_img_path,
            headline=post_data.headline,
            fact_text=post_data.fact_text,
            category=post_data.category_label,
            is_story=True,
        )
        
        raw_img_path.unlink(missing_ok=True)
        
        # Save to history CSV
        try:
            new_row = pd.DataFrame([{
                "timestamp": timestamp,
                "title": post_data.title,
                "category": post_data.category_label,
                "headline": post_data.headline
            }])
            df_history = pd.read_csv(self.history_csv) if self.history_csv.exists() else pd.DataFrame(columns=["timestamp", "title", "category", "headline"])
            df_history = pd.concat([df_history, new_row], ignore_index=True)
            df_history.to_csv(self.history_csv, index=False)
            Messenger.success(f"💾 Added '{post_data.title}' to Facebook Stories history.")
        except Exception as hist_e:
            Messenger.warning(f"⚠️ Failed to save history: {hist_e}")
            
        # Publish if requested
        if publish:
            if not self.fb_tool:
                raise ValueError("❌ Cannot publish: Facebook credentials are missing in .env")
            Messenger.info("🚀 Publishing native Facebook Story to Page...")
            story_id = self.fb_tool.publish_photo_story(composed_img_path)
            Messenger.success(f"🎉 Success! Native Story live on Facebook. ID: {story_id}")
        else:
            Messenger.success(f"💾 Dry-run: Story card saved locally at {composed_img_path}")
            
        return composed_img_path

    def run(self, publish: bool = False, count: int = 1) -> None:
        Messenger.info(f"✨ Starting Facebook Stories Generator (Batch Count: {count}, Publish: {publish})...")
        for i in range(1, count + 1):
            Messenger.info(f"\n--- Processing Story {i}/{count} ---")
            try:
                self.generate_single_story(publish=publish)
                if i < count:
                    time.sleep(3) # Short delay between generations
            except Exception as e:
                Messenger.error(f"💥 Failed generating story {i}: {e}")
                if count == 1:
                    raise e
        Messenger.success(f"🎉 Finished processing {count} Facebook Stories.")
