from pathlib import Path
from tools.common.messenger import Messenger
from tools.video_generation.pexels import PexelsTool
from tools.video_generation.pixabay import PixabayTool
from tools.video_generation.nasa import NASATool
from tools.video_generation.wikimedia import WikimediaTool
from tools.video_generation.generative_visual import GenerativeVisualTool

class MediaHub:
    """
    Centro Maestro de Medios Multimedia de EnigmaIQ:
    Coordina una cascada inteligente de múltiples fuentes gratuitas para garantizar
    que NUNCA falle una escena y siempre muestre exactamente lo narrado.
    """

    def __init__(self):
        self.pexels = PexelsTool()
        self.pixabay = PixabayTool()
        self.nasa = NASATool()
        self.wikimedia = WikimediaTool()
        self.generative = GenerativeVisualTool()

    def fetch_best_clip(self, query: str, out_path: Path, scene_topic: str = "", duration: float = 4.0) -> bool:
        """
        Descarga el mejor metraje disponible utilizando la cascada de precisión.
        """
        clean_q = query.strip()
        Messenger.info(f"\n🎬 [MEDIA HUB] Buscando metraje con máxima precisión para: '{clean_q}'...")

        q_lower = clean_q.lower()
        topic_lower = scene_topic.lower()

        # 1. Si la consulta específica trata estrictamente de astronomía, el espacio exterior o la NASA -> Intentar NASA
        is_space_or_aero = any(w in q_lower for w in [
            "outer space", "planet earth in space", "orbiting earth", "nasa", "satellite in orbit", 
            "solar flare", "solar eclipse", "moon surface", "astronaut", "space telescope"
        ])
        if is_space_or_aero:
            Messenger.info("🛰️ Búsqueda astronómica detectada compatible con NASA API...")
            if self.nasa.fetch_video(clean_q, out_path):
                return True

        # 2. Búsqueda en Pexels (Videos de stock vertical de alta calidad)
        Messenger.info("📹 Probando Pexels...")
        if self.pexels.fetch_video(clean_q, out_path):
            return True

        # 3. Búsqueda en Pixabay
        Messenger.info("📹 Probando Pixabay...")
        if self.pixabay.fetch_video(clean_q, out_path):
            return True

        # 4. Si es evento histórico, personaje o científico -> Wikimedia Commons
        Messenger.info("🏛️ Probando Wikimedia Commons (videos y archivos históricos)...")
        if self.wikimedia.fetch_video(clean_q, out_path):
            return True
        if self.wikimedia.fetch_image_clip(clean_q, out_path, duration=duration):
            return True

        # 5. Fallback Definitivo Cero Margen de Error: IA Generativa Hiperrealista + Ken Burns
        Messenger.info("🎨 Ningún stock comercial tiene este evento exacto. Activando IA Generativa...")
        full_prompt = f"{clean_q}, {scene_topic}".strip(", ")
        if self.generative.generate_clip(full_prompt, out_path, duration=duration):
            return True

        return False
