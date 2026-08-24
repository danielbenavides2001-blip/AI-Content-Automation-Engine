import os
import random
import urllib.request
from pathlib import Path
from typing import Tuple, List, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from tools.common.messenger import Messenger


class StoryCardEngine:
    """
    Advanced Graphic Composition Engine with 5 Viral Layout Templates
    designed specifically for EnigmaIQ (Feed Posts 1080x1350 & Stories 1080x1920).
    Guarantees ZERO text overlap, dynamic Y calculation, and crystal-clear typography.
    """

    FORMAT_MAGNIFIER = "magnifier"
    FORMAT_RED_BANNER = "red_banner"
    FORMAT_SPLIT_SCREEN = "split_screen"
    FORMAT_HIGHLIGHTER = "highlighter"
    FORMAT_CLASSIC_CARD = "classic_card"

    ALL_FORMATS = [
        FORMAT_MAGNIFIER,
        FORMAT_RED_BANNER,
        FORMAT_SPLIT_SCREEN,
        FORMAT_HIGHLIGHTER,
        FORMAT_CLASSIC_CARD,
    ]

    def __init__(self, resource_dir: Optional[Path] = None):
        if resource_dir is None:
            self.resource_dir = Path(__file__).resolve().parent.parent.parent / "flows" / "curiosity_image_generator" / "resources"
        else:
            self.resource_dir = resource_dir
        self.resource_dir.mkdir(parents=True, exist_ok=True)
        self.font_dir = self.resource_dir / "fonts"
        self.font_dir.mkdir(parents=True, exist_ok=True)

    def get_fonts(self) -> Tuple[Path, Path]:
        font_bold = self.font_dir / "Montserrat-Bold.ttf"
        font_medium = self.font_dir / "Montserrat-Medium.ttf"

        url_bold = "https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-Bold.ttf"
        url_medium = "https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-Medium.ttf"

        if not font_bold.exists():
            try:
                Messenger.info("Downloading Montserrat-Bold...")
                urllib.request.urlretrieve(url_bold, font_bold)
            except Exception as e:
                Messenger.warning(f"Could not download bold font: {e}")

        if not font_medium.exists():
            try:
                Messenger.info("Downloading Montserrat-Medium...")
                urllib.request.urlretrieve(url_medium, font_medium)
            except Exception as e:
                Messenger.warning(f"Could not download medium font: {e}")

        return font_bold, font_medium

    def _fit_and_crop(self, img: Image.Image, target_w: int, target_h: int) -> Image.Image:
        w_orig, h_orig = img.size
        scale = max(target_w / w_orig, target_h / h_orig)
        new_w, new_h = int(w_orig * scale), int(h_orig * scale)
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        return resized.crop((left, top, left + target_w, top + target_h))

    def _draw_brand_header(self, draw: ImageDraw.ImageDraw, canvas_w: int, top_y: int, font_bold: ImageFont.ImageFont, category: str = "CURIOSIDADES"):
        """Draws clean EnigmaIQ header badge and category pill."""
        cat_text = f"  {category.upper()[:16]}  "
        cat_bbox = font_bold.getbbox(cat_text)
        cat_w = cat_bbox[2] - cat_bbox[0] + 16
        cat_h = 36
        cat_x = 50

        # Category Pill Badge
        draw.rounded_rectangle(
            [cat_x, top_y, cat_x + cat_w, top_y + cat_h],
            radius=8,
            fill=(8, 16, 28, 220),
            outline=(60, 235, 255, 220),
            width=2,
        )
        draw.text((cat_x + 8, top_y + 5), cat_text.strip(), font=font_bold, fill=(60, 235, 255, 255))

        # EnigmaIQ Brand Mark
        brand_text = "ENIGMAIQ"
        brand_bbox = font_bold.getbbox(brand_text)
        brand_w = brand_bbox[2] - brand_bbox[0]
        brand_x = canvas_w - 50 - brand_w
        draw.text((brand_x + 2, top_y + 7), brand_text, font=font_bold, fill=(0, 0, 0, 180))
        draw.text((brand_x, top_y + 5), brand_text, font=font_bold, fill=(255, 255, 255, 240))

    # ─────────────────────────────────────────────────────────────────────────
    # 1. FORMATO 1: LUPA DE AUMENTO / MAGNIFIER ZOOM
    # ─────────────────────────────────────────────────────────────────────────
    def render_magnifier_zoom(
        self,
        img_path: Path,
        output_path: Path,
        headline: str,
        fact_text: str,
        category: str = "MISTERIO",
        is_story: bool = False,
    ) -> None:
        target_w = 1080
        target_h = 1920 if is_story else 1350

        font_bold_path, font_medium_path = self.get_fonts()
        try:
            f_title = ImageFont.truetype(str(font_bold_path), 46 if is_story else 42)
            f_body = ImageFont.truetype(str(font_medium_path), 30 if is_story else 26)
            f_badge = ImageFont.truetype(str(font_bold_path), 22)
            f_pill = ImageFont.truetype(str(font_bold_path), 20)
        except Exception:
            f_title = f_body = f_badge = f_pill = ImageFont.load_default()

        orig = Image.open(img_path).convert("RGBA")
        canvas = self._fit_and_crop(orig, target_w, target_h)

        # 1. Circular Magnifier Inset
        circle_size = 290 if is_story else 250
        circle_x = target_w - circle_size - 50
        circle_y = 120 if is_story else 70

        center_x, center_y = orig.size[0] // 2, int(orig.size[1] * 0.4)
        zoom_radius = int(min(orig.size) * 0.22)
        box = (
            max(0, center_x - zoom_radius),
            max(0, center_y - zoom_radius),
            min(orig.size[0], center_x + zoom_radius),
            min(orig.size[1], center_y + zoom_radius),
        )
        cropped_zoom = orig.crop(box).resize((circle_size, circle_size), Image.Resampling.LANCZOS)

        # Mask & Glow
        mask = Image.new("L", (circle_size, circle_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, circle_size, circle_size), fill=255)

        glow_pad = 12
        glow_size = circle_size + (glow_pad * 2)
        glow_img = Image.new("RGBA", (glow_size, glow_size), (0, 0, 0, 0))
        draw_glow = ImageDraw.Draw(glow_img)
        draw_glow.ellipse((0, 0, glow_size, glow_size), fill=(0, 0, 0, 160))
        glow_img = glow_img.filter(ImageFilter.GaussianBlur(8))
        canvas.paste(glow_img, (circle_x - glow_pad, circle_y - glow_pad), glow_img)
        canvas.paste(cropped_zoom, (circle_x, circle_y), mask)

        draw = ImageDraw.Draw(canvas)
        draw.ellipse([circle_x, circle_y, circle_x + circle_size, circle_y + circle_size], outline=(255, 255, 255, 255), width=5)
        draw.ellipse([circle_x + 3, circle_y + 3, circle_x + circle_size - 3, circle_y + circle_size - 3], outline=(255, 140, 30, 220), width=3)

        # Pointer line & dot
        dot_x, dot_y = int(target_w * 0.42), int(target_h * 0.40)
        line_start_x = circle_x + 10
        line_start_y = circle_y + circle_size - 20
        draw.line([(line_start_x, line_start_y), (dot_x, dot_y)], fill=(255, 255, 255, 220), width=3)
        draw.ellipse([dot_x - 6, dot_y - 6, dot_x + 6, dot_y + 6], fill=(255, 255, 255, 255), outline=(255, 140, 30, 255), width=3)

        # 2. Bottom Dark Gradient Overlay
        grad_start = int(target_h * 0.52)
        overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)
        for y in range(grad_start, target_h):
            prog = (y - grad_start) / (target_h - grad_start)
            alpha = int(prog * 250)
            draw_ov.line([(0, y), (target_w, y)], fill=(6, 8, 16, alpha))
        canvas = Image.alpha_composite(canvas, overlay)
        draw = ImageDraw.Draw(canvas)

        # Header Brand Top
        self._draw_brand_header(draw, target_w, 80 if is_story else 35, f_badge, category)

        # 3. Center Pill Badge
        pill_y = int(target_h * 0.60) if is_story else int(target_h * 0.58)
        pill_text = f"  ENIGMAIQ • {category.upper()[:16]}  "
        p_bbox = f_pill.getbbox(pill_text)
        p_w = p_bbox[2] - p_bbox[0] + 20
        p_h = 32
        p_x = (target_w - p_w) // 2

        draw.line([(60, pill_y + 16), (target_w - 60, pill_y + 16)], fill=(255, 255, 255, 60), width=2)
        draw.rounded_rectangle([p_x, pill_y, p_x + p_w, pill_y + p_h], radius=16, fill=(255, 110, 20, 255))
        draw.text((p_x + 10, pill_y + 5), pill_text.strip(), font=f_pill, fill=(255, 255, 255, 255))

        # 4. Dynamic Headline (Calculates End Y)
        head_start_y = pill_y + 48
        head_end_y = self._draw_wrapped_headline(
            draw=draw,
            headline=headline,
            font=f_title,
            max_w=target_w - 120,
            start_y=head_start_y,
            canvas_w=target_w,
            highlight_color=(255, 140, 30, 255),
            default_color=(255, 255, 255, 255),
            centered=True,
            line_spacing=50 if is_story else 46,
        )

        # 5. Dynamic Fact Subtitle (NEVER overlaps, starts strictly below headline)
        if fact_text:
            fact_start_y = head_end_y + 16
            if fact_start_y < target_h - 100:
                self._draw_wrapped_text(
                    draw=draw,
                    text=fact_text,
                    font=f_body,
                    max_w=target_w - 140,
                    start_y=fact_start_y,
                    canvas_w=target_w,
                    color=(215, 225, 235, 240),
                    centered=True,
                    line_spacing=36,
                    max_lines=3,
                )

        final = canvas.convert("RGB")
        final.save(output_path, "JPEG", quality=95)
        Messenger.success(f"🎨 Formato [Magnifier Zoom] creado en: {output_path.name}")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. FORMATO 2: ALERTA ROJA / BREAKING NEWS BANNER
    # ─────────────────────────────────────────────────────────────────────────
    def render_red_banner(
        self,
        img_path: Path,
        output_path: Path,
        headline: str,
        fact_text: str,
        category: str = "DESCUBRIMIENTO",
        is_story: bool = False,
    ) -> None:
        target_w = 1080
        target_h = 1920 if is_story else 1350

        font_bold_path, font_medium_path = self.get_fonts()
        try:
            f_banner = ImageFont.truetype(str(font_bold_path), 38 if is_story else 36)
            f_sub = ImageFont.truetype(str(font_bold_path), 42 if is_story else 38)
            f_body = ImageFont.truetype(str(font_medium_path), 28 if is_story else 26)
            f_badge = ImageFont.truetype(str(font_bold_path), 22)
            f_watermark = ImageFont.truetype(str(font_bold_path), 28)
        except Exception:
            f_banner = f_sub = f_body = f_badge = f_watermark = ImageFont.load_default()

        orig = Image.open(img_path).convert("RGBA")
        canvas = self._fit_and_crop(orig, target_w, target_h)

        # Bottom Dark Gradient
        grad_start = int(target_h * 0.48)
        overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)
        for y in range(grad_start, target_h):
            prog = (y - grad_start) / (target_h - grad_start)
            alpha = int(prog * 250)
            draw_ov.line([(0, y), (target_w, y)], fill=(8, 10, 16, alpha))
        canvas = Image.alpha_composite(canvas, overlay)
        draw = ImageDraw.Draw(canvas)

        # Header Brand Top
        self._draw_brand_header(draw, target_w, 80 if is_story else 35, f_badge, category)

        # Watermark
        wm_text = "ENIGMAIQ"
        wm_bbox = f_watermark.getbbox(wm_text)
        wm_w = wm_bbox[2] - wm_bbox[0]
        draw.text(((target_w - wm_w) // 2, int(target_h * 0.40)), wm_text, font=f_watermark, fill=(255, 255, 255, 60))

        # Red Banner Box (Short punchy banner)
        banner_y = int(target_h * 0.58) if is_story else int(target_h * 0.56)
        clean_head = headline.replace("[", "").replace("]", "")
        banner_text = f"¡{clean_head[:36].upper()}!" if len(clean_head) > 36 else f"¡{clean_head.upper()}!"

        banner_pad_y = 12
        b_bbox = f_banner.getbbox(banner_text)
        b_w = min(b_bbox[2] - b_bbox[0] + 36, target_w - 80)
        b_h = b_bbox[3] - b_bbox[1] + (banner_pad_y * 2)
        b_x = (target_w - b_w) // 2

        draw.rectangle([b_x, banner_y, b_x + b_w, banner_y + b_h], fill=(225, 20, 30, 255))
        b_text_x = (target_w - (b_bbox[2] - b_bbox[0])) // 2
        draw.text((b_text_x, banner_y + banner_pad_y - 4), banner_text, font=f_banner, fill=(255, 255, 255, 255))

        # Dynamic Subtitle below Red Banner
        sub_start_y = banner_y + b_h + 24
        sub_end_y = self._draw_wrapped_headline(
            draw=draw,
            headline=headline,
            font=f_sub,
            max_w=target_w - 100,
            start_y=sub_start_y,
            canvas_w=target_w,
            highlight_color=(255, 230, 50, 255),
            default_color=(255, 255, 255, 255),
            centered=True,
            line_spacing=48 if is_story else 44,
        )

        # Dynamic Fact text
        if fact_text and (sub_end_y + 14 < target_h - 80):
            self._draw_wrapped_text(
                draw=draw,
                text=fact_text,
                font=f_body,
                max_w=target_w - 120,
                start_y=sub_end_y + 14,
                canvas_w=target_w,
                color=(220, 230, 240, 230),
                centered=True,
                line_spacing=34,
                max_lines=3,
            )

        final = canvas.convert("RGB")
        final.save(output_path, "JPEG", quality=95)
        Messenger.success(f"🎨 Formato [Red Banner] creado en: {output_path.name}")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. FORMATO 3: PANTALLA DIVIDIDA / COMPARACIÓN DUAL (SPLIT SCREEN)
    # ─────────────────────────────────────────────────────────────────────────
    def render_split_screen(
        self,
        img_path: Path,
        output_path: Path,
        headline: str,
        fact_text: str,
        category: str = "GEOLOGÍA",
        is_story: bool = False,
    ) -> None:
        target_w = 1080
        target_h = 1920 if is_story else 1350

        font_bold_path, font_medium_path = self.get_fonts()
        try:
            f_title = ImageFont.truetype(str(font_bold_path), 44 if is_story else 40)
            f_tag = ImageFont.truetype(str(font_bold_path), 22)
            f_badge = ImageFont.truetype(str(font_bold_path), 22)
            f_body = ImageFont.truetype(str(font_medium_path), 28 if is_story else 24)
        except Exception:
            f_title = f_tag = f_badge = f_body = ImageFont.load_default()

        orig = Image.open(img_path).convert("RGBA")
        split_h = int(target_h * 0.34) if is_story else int(target_h * 0.33)

        upper_panel = self._fit_and_crop(orig, target_w, split_h)
        lower_panel = self._fit_and_crop(orig.crop((0, int(orig.size[1]*0.28), orig.size[0], orig.size[1])), target_w, split_h)

        canvas = Image.new("RGBA", (target_w, target_h), (8, 12, 20, 255))
        canvas.paste(upper_panel, (0, 0))
        canvas.paste(lower_panel, (0, split_h + 6))

        draw = ImageDraw.Draw(canvas)
        draw.line([(0, split_h + 3), (target_w, split_h + 3)], fill=(255, 255, 255, 220), width=3)

        self._draw_panel_tag(draw, 40, 50, "PERSPECTIVA GLOBAL", (60, 235, 255, 255), f_tag)
        self._draw_panel_tag(draw, 40, split_h + 24, "DETALLE CIENTÍFICO", (255, 200, 40, 255), f_tag)

        # Bottom Black Content Area
        content_y = (split_h * 2) + 12
        draw.rectangle([0, content_y, target_w, target_h], fill=(8, 12, 20, 255))

        self._draw_brand_header(draw, target_w, target_h - 50, f_badge, category)

        # Headline with dynamic end Y
        head_end_y = self._draw_wrapped_headline(
            draw=draw,
            headline=headline,
            font=f_title,
            max_w=target_w - 100,
            start_y=content_y + 25,
            canvas_w=target_w,
            highlight_color=(60, 235, 255, 255),
            default_color=(255, 255, 255, 255),
            centered=True,
            line_spacing=46 if is_story else 42,
        )

        if fact_text and (head_end_y + 14 < target_h - 70):
            self._draw_wrapped_text(
                draw=draw,
                text=fact_text,
                font=f_body,
                max_w=target_w - 120,
                start_y=head_end_y + 14,
                canvas_w=target_w,
                color=(205, 220, 235, 230),
                centered=True,
                line_spacing=34,
                max_lines=3,
            )

        final = canvas.convert("RGB")
        final.save(output_path, "JPEG", quality=95)
        Messenger.success(f"🎨 Formato [Split Screen] creado en: {output_path.name}")

    def _draw_panel_tag(self, draw: ImageDraw.ImageDraw, x: int, y: int, text: str, color: Tuple[int, int, int, int], font: ImageFont.ImageFont):
        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0] + 16
        h = bbox[3] - bbox[1] + 10
        draw.rectangle([x, y, x + w, y + h], fill=(0, 0, 0, 190), outline=color, width=2)
        draw.text((x + 8, y + 3), text, font=font, fill=color)

    # ─────────────────────────────────────────────────────────────────────────
    # 4. FORMATO 4: MARCADOR FLUORESCENTE / HIGHLIGHTER TEXT
    # ─────────────────────────────────────────────────────────────────────────
    def render_highlighter_text(
        self,
        img_path: Path,
        output_path: Path,
        headline: str,
        fact_text: str,
        category: str = "HISTORIA",
        is_story: bool = False,
    ) -> None:
        target_w = 1080
        target_h = 1920 if is_story else 1350

        font_bold_path, font_medium_path = self.get_fonts()
        try:
            f_head = ImageFont.truetype(str(font_bold_path), 46 if is_story else 42)
            f_body = ImageFont.truetype(str(font_medium_path), 28 if is_story else 24)
            f_cat_box = ImageFont.truetype(str(font_bold_path), 24)
            f_badge = ImageFont.truetype(str(font_bold_path), 22)
        except Exception:
            f_head = f_body = f_cat_box = f_badge = ImageFont.load_default()

        orig = Image.open(img_path).convert("RGBA")
        canvas = self._fit_and_crop(orig, target_w, target_h)

        # Bottom Dark Gradient
        grad_start = int(target_h * 0.45)
        overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)
        for y in range(grad_start, target_h):
            prog = (y - grad_start) / (target_h - grad_start)
            alpha = int(prog * 240)
            draw_ov.line([(0, y), (target_w, y)], fill=(6, 8, 14, alpha))
        canvas = Image.alpha_composite(canvas, overlay)
        draw = ImageDraw.Draw(canvas)

        # Top Header Brand
        self._draw_brand_header(draw, target_w, 80 if is_story else 35, f_badge, category)

        # Highlighter Headline Words
        words = headline.split()
        parsed = []
        for w in words:
            if w.startswith("[") and w.endswith("]"):
                parsed.append((w[1:-1], True))
            elif w.startswith("[") and (w.endswith("],") or w.endswith("]?") or w.endswith("]!")):
                parsed.append((w[1:-2] + w[-1], True))
            else:
                parsed.append((w, False))

        margin_x = 60
        max_w = target_w - (margin_x * 2)
        start_y = int(target_h * 0.58) if is_story else int(target_h * 0.55)
        line_spacing = 58 if is_story else 52
        space_w = f_head.getbbox(" ")[2] - f_head.getbbox(" ")[0]

        lines = []
        curr_line = []
        curr_w = 0
        for word, is_hl in parsed:
            wb = f_head.getbbox(word)
            w_len = wb[2] - wb[0]
            add_len = w_len + (space_w if curr_line else 0)
            if curr_w + add_len <= max_w:
                curr_line.append((word, is_hl, w_len))
                curr_w += add_len
            else:
                if curr_line:
                    lines.append(curr_line)
                curr_line = [(word, is_hl, w_len)]
                curr_w = w_len
        if curr_line:
            lines.append(curr_line)

        lines = lines[:4] # Max 4 lines of headline to prevent overflow

        for idx, line in enumerate(lines):
            curr_x = margin_x
            line_y = start_y + (idx * line_spacing)

            for word, is_hl, w_len in line:
                if is_hl:
                    box_pad = 5
                    draw.rectangle(
                        [curr_x - box_pad, line_y - 2, curr_x + w_len + box_pad, line_y + 40],
                        fill=(255, 230, 40, 255),
                    )
                    draw.text((curr_x, line_y), word, font=f_head, fill=(10, 10, 10, 255))
                else:
                    draw.text((curr_x + 2, line_y + 2), word, font=f_head, fill=(0, 0, 0, 180))
                    draw.text((curr_x, line_y), word, font=f_head, fill=(255, 255, 255, 255))

                curr_x += w_len + space_w

        head_end_y = start_y + (len(lines) * line_spacing)

        # Dynamic Fact Subtitle
        if fact_text and (head_end_y + 14 < target_h - 90):
            fact_end_y = self._draw_wrapped_text(
                draw=draw,
                text=fact_text,
                font=f_body,
                max_w=target_w - (margin_x * 2),
                start_y=head_end_y + 14,
                canvas_w=target_w,
                color=(210, 220, 235, 230),
                centered=False,
                margin_left=margin_x,
                line_spacing=34,
                max_lines=2,
            )
            cat_box_y = fact_end_y + 18
        else:
            cat_box_y = head_end_y + 18

        # Bottom Yellow Category Rectangle Badge
        cat_str = f"  {category.upper()[:14]} • ENIGMAIQ  "
        c_bbox = f_cat_box.getbbox(cat_str)
        c_w = c_bbox[2] - c_bbox[0] + 16
        c_h = 38
        if cat_box_y + c_h < target_h - 20:
            draw.rectangle([margin_x, cat_box_y, margin_x + c_w, cat_box_y + c_h], fill=(255, 230, 40, 255))
            draw.text((margin_x + 8, cat_box_y + 5), cat_str.strip(), font=f_cat_box, fill=(10, 10, 10, 255))

        final = canvas.convert("RGB")
        final.save(output_path, "JPEG", quality=95)
        Messenger.success(f"🎨 Formato [Highlighter Text] creado en: {output_path.name}")

    # ─────────────────────────────────────────────────────────────────────────
    # 5. FORMATO 5: TARJETA CLÁSICA ¿SABÍAS QUE...? ELEGANTE
    # ─────────────────────────────────────────────────────────────────────────
    def render_classic_card(
        self,
        img_path: Path,
        output_path: Path,
        headline: str,
        fact_text: str,
        category: str = "ENIGMA",
        is_story: bool = False,
    ) -> None:
        target_w = 1080
        target_h = 1920 if is_story else 1350

        font_bold_path, font_medium_path = self.get_fonts()
        try:
            f_title = ImageFont.truetype(str(font_bold_path), 46 if is_story else 44)
            f_head = ImageFont.truetype(str(font_bold_path), 36 if is_story else 32)
            f_body = ImageFont.truetype(str(font_medium_path), 30 if is_story else 26)
            f_badge = ImageFont.truetype(str(font_bold_path), 22)
        except Exception:
            f_title = f_head = f_body = f_badge = ImageFont.load_default()

        orig = Image.open(img_path).convert("RGBA")
        img_h = int(target_h * 0.55) if is_story else int(target_h * 0.55)
        top_img = self._fit_and_crop(orig, target_w, img_h)

        canvas = Image.new("RGBA", (target_w, target_h), (8, 10, 16, 255))
        canvas.paste(top_img, (0, 0))

        draw = ImageDraw.Draw(canvas)
        draw.line([(0, img_h), (target_w, img_h)], fill=(60, 235, 255, 180), width=3)

        self._draw_brand_header(draw, target_w, 80 if is_story else 35, f_badge, category)

        card_start_y = img_h + 30
        margin_x = 60

        # Bulb Icon & "¿SABÍAS QUE...?"
        title_str = "💡 ¿SABÍAS QUE...?"
        draw.text((margin_x + 2, card_start_y + 2), title_str, font=f_title, fill=(0, 0, 0, 180))
        draw.text((margin_x, card_start_y), title_str, font=f_title, fill=(255, 220, 50, 255))

        # Headline summary in cyan / white
        clean_headline = headline.replace("[", "").replace("]", "")
        head_start_y = card_start_y + 60
        head_end_y = self._draw_wrapped_text(
            draw=draw,
            text=clean_headline,
            font=f_head,
            max_w=target_w - (margin_x * 2),
            start_y=head_start_y,
            canvas_w=target_w,
            color=(60, 235, 255, 255),
            centered=False,
            margin_left=margin_x,
            line_spacing=40,
            max_lines=2,
        )

        # Body Explanation Text
        body_start_y = head_end_y + 14
        if fact_text and (body_start_y < target_h - 70):
            self._draw_wrapped_text(
                draw=draw,
                text=fact_text,
                font=f_body,
                max_w=target_w - (margin_x * 2),
                start_y=body_start_y,
                canvas_w=target_w,
                color=(220, 230, 245, 255),
                centered=False,
                margin_left=margin_x,
                line_spacing=36,
                max_lines=4,
            )

        # Footer Brand Tag
        draw.text((margin_x, target_h - 55), "— Publicado por EnigmaIQ", font=f_badge, fill=(60, 235, 255, 180))

        final = canvas.convert("RGB")
        final.save(output_path, "JPEG", quality=95)
        Messenger.success(f"🎨 Formato [Classic Card] creado en: {output_path.name}")

    # ─────────────────────────────────────────────────────────────────────────
    # HELPER: Dynamic Text Rendering with Zero Overlap
    # ─────────────────────────────────────────────────────────────────────────
    def _draw_wrapped_headline(
        self,
        draw: ImageDraw.ImageDraw,
        headline: str,
        font: ImageFont.ImageFont,
        max_w: int,
        start_y: int,
        canvas_w: int,
        highlight_color: Tuple[int, int, int, int],
        default_color: Tuple[int, int, int, int],
        centered: bool = True,
        line_spacing: int = 48,
    ) -> int:
        words_raw = headline.split()
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

        space_w = font.getbbox(" ")[2] - font.getbbox(" ")[0]
        lines = []
        curr_line = []
        curr_width = 0

        for word, is_hl in parsed_words:
            wb = font.getbbox(word)
            w_len = wb[2] - wb[0]
            add_w = w_len + (space_w if curr_line else 0)
            if curr_width + add_w <= max_w:
                curr_line.append((word, is_hl, w_len))
                curr_width += add_w
            else:
                if curr_line:
                    lines.append(curr_line)
                curr_line = [(word, is_hl, w_len)]
                curr_width = w_len
        if curr_line:
            lines.append(curr_line)

        # Max 4 lines of headline
        lines = lines[:4]

        for idx, line in enumerate(lines):
            total_w = sum(item[2] for item in line) + space_w * (len(line) - 1)
            line_x = (canvas_w - total_w) // 2 if centered else 60
            line_y = start_y + (idx * line_spacing)

            curr_x = line_x
            for word, is_hl, w_len in line:
                color = highlight_color if is_hl else default_color
                draw.text((curr_x + 2, line_y + 2), word, font=font, fill=(0, 0, 0, 180))
                draw.text((curr_x, line_y), word, font=font, fill=color)
                curr_x += w_len + space_w

        return start_y + (len(lines) * line_spacing)

    def _draw_wrapped_text(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.ImageFont,
        max_w: int,
        start_y: int,
        canvas_w: int,
        color: Tuple[int, int, int, int],
        centered: bool = True,
        margin_left: int = 60,
        line_spacing: int = 36,
        max_lines: int = 3,
    ) -> int:
        clean_text = text.replace("[", "").replace("]", "")
        words = clean_text.split()
        lines = []
        curr = []
        curr_w = 0
        space_w = font.getbbox(" ")[2] - font.getbbox(" ")[0]

        for w in words:
            wb = font.getbbox(w)
            w_len = wb[2] - wb[0]
            add_w = w_len + (space_w if curr else 0)
            if curr_w + add_w <= max_w:
                curr.append(w)
                curr_w += add_w
            else:
                if curr:
                    lines.append(" ".join(curr))
                curr = [w]
                curr_w = w_len
        if curr:
            lines.append(" ".join(curr))

        lines = lines[:max_lines]

        for idx, line_str in enumerate(lines):
            line_y = start_y + (idx * line_spacing)
            if centered:
                wb = font.getbbox(line_str)
                l_w = wb[2] - wb[0]
                line_x = (canvas_w - l_w) // 2
            else:
                line_x = margin_left
            draw.text((line_x + 1, line_y + 1), line_str, font=font, fill=(0, 0, 0, 160))
            draw.text((line_x, line_y), line_str, font=font, fill=color)

        return start_y + (len(lines) * line_spacing)

    # ─────────────────────────────────────────────────────────────────────────
    # RENDER DISPATCHER
    # ─────────────────────────────────────────────────────────────────────────
    def compose_random_template(
        self,
        img_path: Path,
        output_path: Path,
        headline: str,
        fact_text: str,
        category: str = "MISTERIO",
        is_story: bool = False,
        force_format: Optional[str] = None,
    ) -> str:
        selected_fmt = force_format if force_format in self.ALL_FORMATS else random.choice(self.ALL_FORMATS)
        Messenger.info(f"🎭 Selected Visual Template: [{selected_fmt.upper()}] (Is Story: {is_story})")

        if selected_fmt == self.FORMAT_MAGNIFIER:
            self.render_magnifier_zoom(img_path, output_path, headline, fact_text, category, is_story)
        elif selected_fmt == self.FORMAT_RED_BANNER:
            self.render_red_banner(img_path, output_path, headline, fact_text, category, is_story)
        elif selected_fmt == self.FORMAT_SPLIT_SCREEN:
            self.render_split_screen(img_path, output_path, headline, fact_text, category, is_story)
        elif selected_fmt == self.FORMAT_HIGHLIGHTER:
            self.render_highlighter_text(img_path, output_path, headline, fact_text, category, is_story)
        else:
            self.render_classic_card(img_path, output_path, headline, fact_text, category, is_story)

        return selected_fmt
