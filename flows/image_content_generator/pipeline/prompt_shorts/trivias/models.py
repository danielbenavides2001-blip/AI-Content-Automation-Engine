from typing import List, Type, ClassVar, Optional
from pydantic import BaseModel, Field, model_validator
from flows.image_content_generator.pipeline.prompt_base.models import BaseIdea, CategoryHandler, Scene
from flows.image_content_generator.pipeline.prompt_shorts.trivias import constants as trivia_constants


class TriviaIdea(BaseIdea):
    IDEA_PROMPT: ClassVar[str] = trivia_constants.IDEA_PROMPT_TRIVIAS
    intrigue_header: str = Field(description="A short, punchy 3-5 word phrase to persist at the top of the video in ALL CAPS to create extreme intrigue (e.g., 'DESAFÍO ORTOGRÁFICO', 'TRIVIA DE FÚTBOL').")
    caption: str = Field(description="Una descripción para redes sociales altamente viral e interactiva sobre la trivia presentada. DEBE incluir entre 5 y 8 hashtags extremadamente virales (Ej: #Trivia #Desafio #Ortografia #Futbol #Curiosidades #Quiz).")
    category: str = "trivias"


class TriviaScene(Scene):
    question: str = Field(default="", description="El texto de la pregunta de trivia que aparecerá en pantalla (Vacío en intros/outros).")
    options: List[str] = Field(default_factory=list, description="Lista de exactamente 4 opciones de respuesta formateadas como A, B, C, D (Vacío en intros/outros).")
    correct_answer: str = Field(default="", description="La opción correcta de la lista (Vacío en intros/outros).")
    narration_question: str = Field(default="", description="Locución entusiasta e intrigante de la pregunta planteada, o locución completa de intros/outros.")
    narration_answer: str = Field(default="", description="Locución gratificante e informativa revelando la respuesta (Vacío en intros/outros).")
    
    # Timing metadata dynamically updated in the audio step
    q_dur: float = Field(default=0.0, description="Duración en segundos del audio de la pregunta.")
    a_dur: float = Field(default=0.0, description="Duración en segundos del audio de la respuesta.")
    duration: float = Field(default=0.0, description="Duración total en segundos de la escena.")
    
    narration: str = Field(default="", description="Locución completa unificada (auto-generada).")
    sfx: str = Field(default="none", description="Efecto de sonido ambiental o transición para la escena ('digital_swoosh', 'ocean_waves', 'jungle_ambient', o 'none').")

    @model_validator(mode='after')
    def build_narration(self) -> 'TriviaScene':
        if self.narration_answer:
            self.narration = f"{self.narration_question} ... {self.narration_answer}"
        else:
            self.narration = self.narration_question
        return self


class TriviasHandler(CategoryHandler):
    category: str = "trivias"
    idea_variants: ClassVar[List[Type[BaseIdea]]] = [TriviaIdea]
    scenes: List[TriviaScene] = Field(description="List of scenes detailing the trivia script")
