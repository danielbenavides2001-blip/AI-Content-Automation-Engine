from typing import List, Type, ClassVar
from flows.image_content_generator.pipeline.prompt_base.models import BaseIdea, CategoryHandler
from flows.image_content_generator.pipeline.prompt_shorts.football import constants as football_constants
from pydantic import Field

class FootballIdea(BaseIdea):
    IDEA_PROMPT: ClassVar[str] = football_constants.IDEA_PROMPT_FOOTBALL
    top_headline: str = Field(description="Un titular de curiosidad extrema en MAYÚSCULAS para el video (ej., 'UN PERRO SALVÓ EL MUNDIAL DE 1966'). Estático, en Negrita, en Mayúsculas.")
    caption: str = Field(description="Un caption/descripción altamente viral e intrigante en español que invite a los comentarios. DEBE incluir de 5 a 8 hashtags muy virales (ej., #Fútbol #Mundial #EnigmaIQ).")

class FootballHandler(CategoryHandler):
    category: str = "football"
    idea_variants: ClassVar[List[Type[BaseIdea]]] = [FootballIdea]
