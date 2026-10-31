from typing import List, Type, ClassVar, Optional
from flows.image_content_generator.pipeline.prompt_base.models import BaseIdea, CategoryHandler, Scene, VideoScript
from flows.image_content_generator.pipeline.prompt_shorts.como_funciona import constants as como_funciona_constants
from pydantic import Field, ConfigDict

class ComoFuncionaIdea(BaseIdea):
    IDEA_PROMPT: ClassVar[str] = como_funciona_constants.IDEA_PROMPT_COMO_FUNCIONA
    header_title: str = Field(
        default="MECÁNICA ENIGMAIQ",
        description="Frase técnica corta de 2-4 palabras en MAYÚSCULAS para encabezado elegante y minimalista arriba (ej: 'MECÁNICA INTERNA', 'ANATOMÍA OCULTA', 'FÍSICA VISUAL')."
    )
    caption: str = Field(
        description="Descripción intrigante para Facebook/Instagram con 4-5 hashtags limpios (#ciencia #mecanica #curiosidades #datoscuriosos #enigmaiq)."
    )

class ComoFuncionaScene(Scene):
    model_config = ConfigDict(extra='ignore')
    sfx: Optional[str] = Field(default="mechanical_click", description="Efecto de sonido breve para el corte o acción física")

class ComoFuncionaScript(VideoScript):
    model_config = ConfigDict(extra='ignore')
    SCRIPT_PROMPT: ClassVar[str] = como_funciona_constants.SCRIPT_PROMPT_COMO_FUNCIONA
    scenes: List[ComoFuncionaScene]

class ComoFuncionaHandler(CategoryHandler):
    category: str = "como_funciona"
    idea_variants: ClassVar[List[Type[BaseIdea]]] = [ComoFuncionaIdea]
