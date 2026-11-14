import os
import sys
import json
import math
import wave
import random
import shutil
import argparse
import datetime
import subprocess
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field
import requests
from dotenv import load_dotenv

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[3]
REMOTION_DIR = BASE_DIR / "flows" / "image_content_generator" / "remotion"
PUBLIC_DIR = REMOTION_DIR / "public"
AUDIO_DIR = PUBLIC_DIR / "dynamic_audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR = PUBLIC_DIR / "dynamic_videos"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "automated_posts_history.csv"

from tools.common.messenger import Messenger
from tools.text_generation.gemini import GeminiTextGenerator
from tools.audio_generation.gemini import GeminiAudioGenerator
from tools.video_generation.pexels import PexelsTool
from tools.video_generation.pixabay import PixabayTool
from tools.video_generation.media_hub import MediaHub

# ==============================================================================
# PYDANTIC SCHEMAS FOR STRUCTURED GEMINI BLUEPRINT GENERATION
# ==============================================================================
class SceneSchema(BaseModel):
    sceneNumber: int = Field(description="Sequential number of the scene (1 to 5)")
    visualArchetype: str = Field(
        description="Must be one of: 'stock_footage', 'country_map', 'dual_country_clash', 'geological_cross_section', 'technical_blueprint', 'telemetry_gauge', 'community_poll'"
    )
    narration: str = Field(
        description="Spoken narration script in Spanish. MUST be between 22 and 26 words with scientific precision, punchy rhythm, and narrative intrigue."
    )
    headline: str = Field(
        description="Punchy uppercase HUD title (2-4 words, e.g. 'ANOMALÍA GEOLÓGICA', 'COLOMBIA VS ECUADOR', 'PRESIÓN EXTREMA')"
    )
    subheadline: str = Field(
        description="Uppercase secondary explanatory text (e.g. 'DENSIDAD BOTÁNICA SIN PRECEDENTES', '35 GRAMOS POR LITRO')"
    )
    stockQuery: str = Field(
        description="Short 2-4 word English search query to find the exact matching vertical stock video on Pexels/Pixabay showing what is being narrated (e.g. 'ocean waves storm', 'rain mountain forest', 'amazon river jungle aerial', 'volcano lava eruption', 'underwater deep sea', 'lightning storm dark sky', 'satellite earth rotation')"
    )
    countryA: Optional[str] = Field(
        default=None,
        description="Country A name if mentioning a country (e.g. 'colombia', 'mexico', 'usa', 'ecuador', 'brasil', 'peru', 'chile', 'argentina', 'venezuela')"
    )
    countryB: Optional[str] = Field(
        default=None,
        description="Country B name for comparisons (e.g. 'ecuador', 'usa', 'mexico')"
    )
    metricLabel: Optional[str] = Field(
        default=None,
        description="Short metric label (e.g. 'DIVERSIDAD TOTAL', 'PROFUNDIDAD', 'VOLTAJE', 'DENSIDAD DE SAL')"
    )
    metricValA: Optional[str] = Field(
        default=None,
        description="Metric value for Country A or primary element (e.g. '4.270+', '3.500 m', '10.000 A', '35 g / L')"
    )
    metricValB: Optional[str] = Field(
        default=None,
        description="Metric value for Country B (e.g. '4.000+', '1.200 m')"
    )
    pollOptionA: Optional[str] = Field(
        default=None,
        description="Call-to-action Option A for community poll (e.g. 'COLOMBIA (Por cantidad total)', 'SÍ, YA LO SABÍA')"
    )
    pollOptionB: Optional[str] = Field(
        default=None,
        description="Call-to-action Option B for community poll (e.g. 'ECUADOR (Por densidad por km²)', 'NO, ME ACABO DE ENTERAR')"
    )

class DynamicBlueprintSchema(BaseModel):
    title: str = Field(description="Sensational, viral, scientifically accurate video title")
    category: str = Field(
        description="Category tag, e.g. 'FENÓMENOS PLANETARIOS', 'CÓMO FUNCIONA', 'COMPARATIVA DE PAÍSES', 'CURIOSIDADES DE PAÍSES', 'SABÍAS QUÉ'"
    )
    pillar: str = Field(
        description="Pillar name: 'curiosidades_fenomenos', 'como_funciona', 'comparativa_paises', 'curiosidades_pais', 'sabias_que'"
    )
    primaryColor: str = Field(
        default="#00f5ff",
        description="Hex primary cyber neon color (e.g. '#00f5ff', '#38bdf8', '#10b981', '#f59e0b', '#ec4899')"
    )
    secondaryColor: str = Field(default="#38bdf8", description="Hex secondary cyber color")
    accentColor: str = Field(default="#f59e0b", description="Hex accent highlight color (gold '#f59e0b')")
    backgroundColor: str = Field(default="#030814", description="Deep dark futuristic background color")
    scenes: List[SceneSchema] = Field(
        description="List of exactly 5 scenes. The LAST scene (Scene 5) must always be 'community_poll'."
    )
    facebookDescription: str = Field(
        description="High-converting Facebook post description with emojis, summary, EnigmaIQ call to action, and 8-12 relevant hashtags."
    )

# ==============================================================================
# AUTONOMOUS ENGINE
# ==============================================================================
class AutonomousAIRemotionEngine:
    def __init__(self):
        self.text_gen = GeminiTextGenerator()
        self.audio_gen = GeminiAudioGenerator()
        self.pexels = PexelsTool()
        self.pixabay = PixabayTool()
        self.media_hub = MediaHub()

    def get_recent_topics(self) -> str:
        """Reads recent topics to strictly avoid repetition."""
        topics = []
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    lines = f.readlines()[1:]
                    for line in lines[-20:]:
                        parts = line.strip().split(",")
                        if len(parts) >= 3:
                            topics.append(parts[2])
            except Exception as e:
                Messenger.warning(f"Error reading history: {e}")
        return "; ".join(topics) if topics else "Ninguno registrado aún."

    def select_pillar_and_generate_blueprint(self, forced_topic: Optional[str] = None, forced_pillar: Optional[str] = None) -> DynamicBlueprintSchema:
        """Prompts Gemini to conceive a viral, unique topic with exact scene breakdowns."""
        recent = self.get_recent_topics()
        
        pillars_pool = [
            ("curiosidades_fenomenos", "FENÓMENOS PLANETARIOS & QUÍMICOS (anomalías de la Tierra, océanos, atmósfera, volcanes, clima extremo como Catatumbo, salinidad del mar, Chimborazo cerca del Sol)"),
            ("como_funciona", "CÓMO FUNCIONAN CIERTOS ELEMENTOS (mecanismos internos del planeta, física oceánica, ingeniería colosal como por qué el Amazonas no tiene puentes, biología celular como el ajolote o la medusa inmortal)"),
            ("comparativa_paises", "COMPARATIVA ENTRE PAÍSES (enfrentamiento directo de datos entre dos naciones con siluetas de mapa vectoriales y stock real, ej: Colombia vs Ecuador, México vs Estados Unidos, Brasil vs Colombia)"),
            ("curiosidades_pais", "CURIOSIDADES DE UN PAÍS (récord geográfico, enigma o fenómeno extremo de Colombia, México, Estados Unidos, etc. con silueta de mapa y metraje real)"),
            ("sabias_que", "SABÍAS QUÉ (hechos desconcertantes de la ciencia que desafían la intuición: Punto Nemo, el núcleo de la Tierra que gira a diferente velocidad, etc.)")
        ]
        
        if forced_pillar:
            chosen_pillar, chosen_desc = next((p for p in pillars_pool if p[0] == forced_pillar), random.choice(pillars_pool))
        else:
            chosen_pillar, chosen_desc = random.choice(pillars_pool)
            
        Messenger.info(f"🎯 [Pilar Autónomo Seleccionado]: {chosen_pillar.upper()} -> {chosen_desc}")

        prompt = f"""
Eres el Director Creativo Principal y Guionista de 'EnigmaIQ', la marca líder en divulgación científica, cartografía y misterios del planeta al estilo 'El porqué de todo'.
Diseña un guión audiovisual 100% INÉDITO, FASCINANTE Y DE MÁXIMA CALIDAD VISUAL.

PILAR TEMÁTICO ASIGNADO:
{chosen_desc}

{f"TEMA ESPECÍFICO SOLICITADO: {forced_topic}" if forced_topic else "SELECCIONA UN TEMA TOTALMENTE NUEVO, VIRAL Y ASOMBROSO DE ESTE PILAR."}

TEMAS RECIENTES QUE DEBES EVITAR ABSOLUTAMENTE (NO REPETIR):
{recent}

REGLAS CRÍTICAS DE DURACIÓN (ENTRE 63 Y 78 SEGUNDOS > 60s OBLIGATORIO):
1. El video DEBE constar de exactamente 5 escenas consecutivas.
2. Cada escena DEBE tener una narración hablada en español neutro de entre 22 y 26 palabras concisas, rítmicas y con intriga científica.
3. El conteo total de palabras habladas del video DEBE estar entre 115 y 130 palabras. Con la cadencia del locutor (1.7 palabras/segundo), esto garantiza que el video final dure exactamente entre 65 y 78 segundos (> 60s obligatorio, dentro del límite de Reels).
4. La Escena 5 DEBE ser SIEMPRE 'community_poll' cerrando con una pregunta de debate a la audiencia entre pollOptionA y pollOptionB.

REGLAS DE ILUSTRACIÓN VISUAL (SE DEBE MOSTRAR LO QUE SE ESTÁ NARRANDO):
- Para CADA una de las 5 escenas debes asignar un 'stockQuery' en INGLÉS (2-4 palabras) para descargar automáticamente el video de stock real vertical en Pexels/Pixabay que muestre exactamente lo que se narra (ej: 'amazon river jungle aerial', 'heavy storm rain drops', 'deep ocean blue water', 'mountain snow peak clouds', 'volcano lava night', 'cell division microscope').
- Visual Archetype:
  * 'stock_footage': Metraje cinematográfico real de stock con tarjeta de texto upper-third (#0b172a navy + #f59e0b border) y métrica central. Ideal para fenómenos, naturaleza, agua, lluvia, tormentas, experimentos.
  * 'country_map': Cuando se mencione un país específico (Colombia, Ecuador, México, Estados Unidos, Brasil, Perú, Chile, Argentina, Venezuela). Mostrará la silueta del país sobre el video de stock.
  * 'dual_country_clash': Cuando se comparen dos naciones enfrentadas.
  * 'geological_cross_section': Cuando se expliquen capas subterráneas, fallas tectónicas o magma.
  * 'technical_blueprint': Cuando se expliquen mecanismos, ingeniería de estructuras o fuerzas físicas.
  * 'telemetry_gauge': Cuando se expongan métricas extremas, voltajes o presiones.
  * 'community_poll': La ÚLTIMA escena (Escena 5) DEBE ser SIEMPRE 'community_poll'.

PALETA DE COLORES:
Elige colores cyberpunk elegantes (dorado '#f59e0b' para el pill ENIGMAIQ y acentos, cian '#00f5ff', azul cielo '#38bdf8', esmeralda '#10b981') sobre fondo ultra oscuro '#030814'.

Genera la respuesta estrictamente en el formato de esquema JSON solicitado.
"""
        Messenger.info("🧠 Consultando a Gemini para concebir el blueprint visual del video...")
        blueprint = self.text_gen.generate_text(prompt=prompt, schema=DynamicBlueprintSchema)
        Messenger.success(f"🎬 Blueprint concebido con éxito: '{blueprint.title}' ({len(blueprint.scenes)} escenas)")
        return blueprint

    def _get_audio_duration_seconds(self, file_path: Path) -> float:
        """Measures audio duration via ffprobe or wave fallback."""
        try:
            cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(file_path)
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(res.stdout.strip())
        except Exception:
            if str(file_path).endswith(".wav"):
                try:
                    with wave.open(str(file_path), "rb") as wf:
                        return wf.getnframes() / float(wf.getframerate())
                except Exception:
                    pass
            return 14.0

    def _synthesize_scene_audio(self, text: str, wav_path: Path, mp3_path: Path) -> tuple[str, float]:
        """
        Synthesizes speech with cascading resilience:
        1. Primary: Gemini TTS (official 'Fenrir' voice).
        2. Fallback: Edge-TTS ('es-CO-GonzaloNeural' - deep, natural documentary narrator).
        Returns relative audio path for Remotion and measured duration in seconds.
        """
        # Try 1: Gemini TTS
        try:
            self.audio_gen.text_to_speech(text, wav_path)
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(wav_path), "-b:a", "192k", str(mp3_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            final_audio_rel = f"dynamic_audio/{mp3_path.name}"
            with wave.open(str(wav_path), "rb") as wf:
                duration_sec = wf.getnframes() / float(wf.getframerate())
            return final_audio_rel, duration_sec
        except Exception as e:
            Messenger.warning(f"⚠️ Gemini TTS no disponible o cuota agotada ({e}). Activando Neural Fallback...")

        # Try 2: Edge-TTS (es-CO-GonzaloNeural - 100% free, unlimited, zero-quota)
        try:
            import asyncio
            import edge_tts
            async def _run_edge():
                comm = edge_tts.Communicate(text, "es-CO-GonzaloNeural")
                await comm.save(str(mp3_path))
            asyncio.run(_run_edge())
            
            duration_sec = self._get_audio_duration_seconds(mp3_path)
            final_audio_rel = f"dynamic_audio/{mp3_path.name}"
            Messenger.success(f"🔊 Audio generado con Neural Fallback (es-CO-GonzaloNeural): {duration_sec:.1f}s")
            return final_audio_rel, duration_sec
        except Exception as e2:
            Messenger.error(f"❌ Fallback Neural TTS falló: {e2}")
            raise e2

    def _download_scene_stock_video(self, query: str, scene_num: int, scene_topic: str = "", duration: float = 4.0) -> tuple[str, bool]:
        """
        Downloads vertical HD stock video for the scene using MediaHub multi-source cascade.
        Falls back to curated stock assets if external download fails.
        """
        clean_query = query.strip() if query else "nature science ocean"
        video_filename = f"scene_{scene_num}.mp4"
        video_path = VIDEO_DIR / video_filename
        video_rel_path = f"dynamic_videos/{video_filename}"

        Messenger.info(f"   🎥 Buscando metraje con MediaHub para Escena {scene_num}: '{clean_query}'...")
        
        try:
            success = self.media_hub.fetch_best_clip(clean_query, video_path, scene_topic=scene_topic, duration=duration)
            if success and video_path.exists() and video_path.stat().st_size > 10000:
                Messenger.success(f"   ✅ Video obtenido con MediaHub para Escena {scene_num} ({video_path.stat().st_size / 1024:.1f} KB)")
                return video_rel_path, True
        except Exception as e:
            Messenger.warning(f"   ⚠️ Error en MediaHub: {e}")

        # Fallback from existing curated library (mar_salado_assets)
        fallback_candidates = list((PUBLIC_DIR / "mar_salado_assets").glob("scene*.mp4"))
        if fallback_candidates:
            chosen = fallback_candidates[(scene_num - 1) % len(fallback_candidates)]
            shutil.copy(chosen, video_path)
            Messenger.info(f"   🛡️ Video de stock asignado desde assets de alta calidad: {chosen.name}")
            return video_rel_path, True

        return "", False

    def generate_scene_audio_and_timelines(self, blueprint: DynamicBlueprintSchema) -> dict:
        """
        Generates audio files and downloads matching stock videos for every scene,
        computes exact durations, and constructs the complete frame-perfect Remotion blueprint.
        """
        Messenger.info("🎙️ Generando locución y metraje de stock escena por escena...")
        processed_scenes = []
        current_frame = 0
        total_audio_sec = 0.0

        for idx, scene in enumerate(blueprint.scenes):
            scene_num = idx + 1
            audio_base_name = f"dynamic_scene_{scene_num}"
            wav_path = AUDIO_DIR / f"{audio_base_name}.wav"
            mp3_path = AUDIO_DIR / f"{audio_base_name}.mp3"
            
            Messenger.info(f"   ► Escena {scene_num}/{len(blueprint.scenes)}: {scene.visualArchetype} ({len(scene.narration.split())} palabras)")
            
            # 1. Locución
            final_audio_rel, duration_sec = self._synthesize_scene_audio(scene.narration, wav_path, mp3_path)
            total_audio_sec += duration_sec
            
            # 2. Metraje de stock real con MediaHub ("se debe mostrar lo que se esta narrando")
            stock_rel, _ = self._download_scene_stock_video(
                scene.stockQuery,
                scene_num,
                scene_topic=blueprint.title,
                duration=duration_sec
            )
            
            # Frame allocation: duration in frames + 15 frames padding for smooth scene transitions
            duration_frames = int(math.ceil((duration_sec + 0.5) * 30))
            
            scene_dict = {
                "sceneNumber": scene_num,
                "visualArchetype": scene.visualArchetype,
                "startFrame": current_frame,
                "durationFrames": duration_frames,
                "audioPath": final_audio_rel,
                "stockVideoPath": stock_rel,
                "stockQuery": scene.stockQuery,
                "narration": scene.narration,
                "headline": scene.headline,
                "subheadline": scene.subheadline,
                "countryA": scene.countryA or "colombia",
                "countryB": scene.countryB or "ecuador",
                "metricLabel": scene.metricLabel or "",
                "metricValA": scene.metricValA or "",
                "metricValB": scene.metricValB or "",
                "pollOptionA": scene.pollOptionA or "Opción A",
                "pollOptionB": scene.pollOptionB or "Opción B",
            }
            processed_scenes.append(scene_dict)
            current_frame += duration_frames

        # Ensure total duration strictly exceeds 60 seconds (1800 frames @ 30 FPS)
        if current_frame < 1850:
            diff = 1850 - current_frame
            Messenger.warning(f"⚠️ Duración ({current_frame} frames / {current_frame/30:.1f}s) inferior a 61.6s. Añadiendo {diff} frames de pausa al debate final.")
            processed_scenes[-1]["durationFrames"] += diff
            current_frame = 1850

        total_seconds = current_frame / 30.0
        Messenger.success(f"⏱️ Locución total completada: {total_audio_sec:.1f}s de voz pura | Video final: {total_seconds:.2f}s ({current_frame} frames) [> 60s Garantizado]")

        final_blueprint = {
            "title": blueprint.title,
            "category": blueprint.category,
            "pillar": blueprint.pillar,
            "colorTheme": {
                "primary": blueprint.primaryColor,
                "secondary": blueprint.secondaryColor,
                "accent": blueprint.accentColor,
                "background": blueprint.backgroundColor,
            },
            "fps": 30,
            "totalFrames": current_frame,
            "scenes": processed_scenes,
            "facebookDescription": blueprint.facebookDescription
        }

        # Save to remotion/public/dynamic_blueprint.json for Remotion props
        blueprint_file = PUBLIC_DIR / "dynamic_blueprint.json"
        with open(blueprint_file, "w", encoding="utf-8") as f:
            json.dump(final_blueprint, f, indent=2, ensure_ascii=False)
        Messenger.info(f"💾 Blueprint guardado en: {blueprint_file}")
        
        return final_blueprint

    def render_video(self, blueprint_dict: dict) -> Path:
        """Renders the video using Remotion CLI and EnigmaIQDynamicMaster composition."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = BASE_DIR / "flows" / "image_content_generator" / "out_short"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_mp4 = out_dir / f"EnigmaIQ_Dynamic_{timestamp}.mp4"

        Messenger.info(f"🎬 Renderizando EnigmaIQDynamicMaster vía Remotion ({blueprint_dict['totalFrames']} frames)...")
        
        cmd = [
            "npx", "remotion", "render",
            "src/index.ts",
            "EnigmaIQDynamicMaster",
            str(out_mp4),
            "--props=public/dynamic_blueprint.json",
            "--concurrency=4"
        ]
        is_win = sys.platform.startswith("win")
        subprocess.run(cmd, cwd=str(REMOTION_DIR), check=True, shell=is_win)

        if not out_mp4.exists() or out_mp4.stat().st_size < 1000000:
            raise RuntimeError(f"Error en renderizado: El archivo no existe o es demasiado pequeño: {out_mp4}")

        size_mb = out_mp4.stat().st_size / (1024 * 1024)
        Messenger.success(f"✅ Video generado con éxito: {out_mp4.name} ({size_mb:.2f} MB)")
        return out_mp4

    def publish_to_facebook(self, video_path: Path, title: str, description: str):
        """Uploads video to Facebook Reels using Meta Graph API."""
        page_id = os.getenv("FACEBOOK_PAGE_ID", "976163608905137")
        access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")

        if not access_token:
            Messenger.warning("⚠️ Sin FACEBOOK_PAGE_ACCESS_TOKEN. Omitiendo publicación en Facebook.")
            return None

        file_size = video_path.stat().st_size
        base_url = "https://graph.facebook.com/v19.0"

        Messenger.info(f"📤 Publicando Reel dinámico en EnigmaIQ (Página {page_id})...")
        # 1. Start
        start_res = requests.post(
            f"{base_url}/{page_id}/video_reels",
            json={"upload_phase": "start", "access_token": access_token}
        )
        start_res.raise_for_status()
        start_data = start_res.json()
        video_id = start_data["video_id"]
        upload_url = start_data["upload_url"]

        # 2. Transfer
        headers = {
            "Authorization": f"OAuth {access_token}",
            "offset": "0",
            "file_size": str(file_size)
        }
        with open(video_path, "rb") as f:
            upload_res = requests.post(upload_url, headers=headers, data=f.read())
            upload_res.raise_for_status()

        # 3. Finish
        finish_payload = {
            "upload_phase": "finish",
            "access_token": access_token,
            "video_id": video_id,
            "video_state": "PUBLISHED",
            "description": description,
            "title": title
        }
        finish_res = requests.post(f"{base_url}/{page_id}/video_reels", json=finish_payload)
        finish_res.raise_for_status()
        post_data = finish_res.json()
        Messenger.success(f"🎉 ¡Reel publicado exitosamente en EnigmaIQ! Post ID: {post_data}")
        return post_data

    def record_history(self, title: str, duration_sec: float, post_id: str = ""):
        """Records the published video into automated_posts_history.csv."""
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        today = datetime.date.today().isoformat()
        clean_title = title.replace(",", " - ").strip()
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"{today},video_dynamic,{clean_title} ({duration_sec:.1f}s) {post_id}\n")
        Messenger.info(f"📝 Historial actualizado con: '{clean_title}'")

    def run(self, forced_topic: Optional[str] = None, forced_pillar: Optional[str] = None, no_upload: bool = False):
        """Full end-to-end execution pipeline."""
        Messenger.info("==================================================================")
        Messenger.info("🚀 INICIANDO ENIGMAIQ AUTONOMOUS AI REMOTION ENGINE (> 60s)")
        Messenger.info("==================================================================")
        
        # 1. Gemini conceives topic and scenes
        blueprint = self.select_pillar_and_generate_blueprint(forced_topic, forced_pillar)
        
        # 2. TTS Voiceover, Stock Video download & timeline calculation (>60s guarantee)
        blueprint_dict = self.generate_scene_audio_and_timelines(blueprint)
        
        # 3. Remotion dynamic rendering
        video_path = self.render_video(blueprint_dict)
        
        # 4. Meta Graph API Reel publishing
        post_id = ""
        if not no_upload:
            post_result = self.publish_to_facebook(
                video_path=video_path,
                title=blueprint_dict["title"],
                description=blueprint_dict["facebookDescription"]
            )
            if post_result and "id" in post_result:
                post_id = post_result["id"]
        else:
            Messenger.info("ℹ️ Modo no-upload activo: Se omite subida a Facebook.")

        # 5. History tracking
        total_sec = blueprint_dict["totalFrames"] / 30.0
        self.record_history(blueprint_dict["title"], total_sec, post_id)
        Messenger.success("🏁 ¡Flujo autónomo completado con éxito!")

def main():
    parser = argparse.ArgumentParser(description="EnigmaIQ Autonomous AI Remotion Engine")
    parser.add_argument("--topic", type=str, default="", help="Forzar un tema específico o dejar vacío para selección autónoma por Gemini")
    parser.add_argument("--pillar", type=str, default="", help="Forzar un pilar ('curiosidades_fenomenos', 'como_funciona', 'comparativa_paises', 'curiosidades_pais', 'sabias_que')")
    parser.add_argument("--no-upload", action="store_true", help="Omitir subida a Facebook")
    args = parser.parse_args()

    engine = AutonomousAIRemotionEngine()
    engine.run(
        forced_topic=args.topic.strip() if args.topic else None,
        forced_pillar=args.pillar.strip() if args.pillar else None,
        no_upload=args.no_upload
    )

if __name__ == "__main__":
    main()
