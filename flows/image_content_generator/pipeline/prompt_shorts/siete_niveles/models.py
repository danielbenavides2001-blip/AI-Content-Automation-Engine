from typing import ClassVar, List, Optional, Type

from pydantic import Field, model_validator

from flows.image_content_generator.pipeline.prompt_base.models import BaseIdea, CategoryHandler, Scene
from flows.image_content_generator.pipeline.prompt_shorts.siete_niveles import constants as sn_constants


class SieteNivelesIdea(BaseIdea):
    IDEA_PROMPT: ClassVar[str] = sn_constants.IDEA_PROMPT_SIETE_NIVELES
    intrigue_header: str = Field(description="Frase corta de intriga de 3-5 palabras que enganche al espectador")
    caption: str = Field(description="Descripción para redes sociales con hashtags y llamado a la acción")
    category: str = "siete_niveles"


NIVEL_PREFIXES = {
    0: ("",),  # intro scene: no prefix enforcement
    1: ("Nivel 1:", "Empezamos en el nivel 1:"),
    2: ("Subimos al nivel 2:",),
    3: ("Llegamos al nivel 3:",),
    4: ("El nivel 4 es aún más impactante:",),
    5: ("El nivel 5 es donde las cosas se ponen",),
    6: ("El nivel 6 nos lleva al límite:",),
    7: ("Y llegamos al nivel final, el nivel 7:",),
}


def _ensure_nivel_prefix(narration: str, nivel: int) -> str:
    if nivel == 0:
        return str(narration)
    prefixes = NIVEL_PREFIXES.get(nivel, ())
    for prefix in prefixes:
        if str(narration).strip().startswith(prefix):
            return str(narration)
    forced = f"{prefixes[0]} {str(narration).strip()}"
    return forced


class SieteNivelesScene(Scene):
    nivel: int = Field(description="0=intro, o del 1 al 7 para los niveles")
    titulo_nivel: str = Field(default="", description="Nombre exacto del sujeto, criatura, artefacto o lugar de este nivel (ej: 'Titanis', 'Bóveda de Svalbard', 'Manuscrito Voynich')")
    visual_type: str = Field(default="ai_image", description="Usa 'ai_image' para criaturas, fósiles, reliquias, misterios, bóvedas o escenas específicas. 'stock_video' SOLO para naturaleza ambiental genérica moderna (olas, cielo).")
    impacto: str = Field(default="Bajo", description="Factor de impacto: Bajo, Medio, Alto, Extremo")
    sfx: str = Field(default="none", description="Efecto de sonido para la escena")

    @model_validator(mode="after")
    def _validate_scene_coherence(self):
        import re
        self.narration = _ensure_nivel_prefix(self.narration, self.nivel)
        
        # Si titulo_nivel está vacío y nivel > 0, extraer sujeto principal de la narración
        if self.nivel > 0 and (not self.titulo_nivel or not self.titulo_nivel.strip()):
            clean_narr = self.narration
            for p in NIVEL_PREFIXES.get(self.nivel, ()):
                clean_narr = clean_narr.replace(p, "")
            parts = re.split(r'[:.,;]', clean_narr.strip())
            candidate = parts[0].strip() if parts else ""
            candidate = re.sub(r'^(el|la|los|las|un|una)\s+', '', candidate, flags=re.IGNORECASE).strip()
            if candidate and len(candidate) < 60:
                self.titulo_nivel = candidate

        # En los 7 niveles (nivel 1 al 7), forzar 'ai_image' para garantizar fidelidad absoluta
        if self.nivel > 0 and self.visual_type == "stock_video":
            q_lower = (self.pexels_query or "").lower()
            generic_keywords = ["ocean", "waves", "desert", "stars", "clouds", "storm", "sky"]
            if not any(w in q_lower for w in generic_keywords):
                self.visual_type = "ai_image"
                self.pexels_query = ""

        return self


class SieteNivelesHandler(CategoryHandler):
    category: str = "siete_niveles"
    idea_variants: ClassVar[List[Type[BaseIdea]]] = [SieteNivelesIdea]
    scenes: List[SieteNivelesScene]

    @model_validator(mode="after")
    def _ensure_all_prefixes(self):
        for scene in self.scenes:
            scene.narration = _ensure_nivel_prefix(scene.narration, scene.nivel)
        return self
