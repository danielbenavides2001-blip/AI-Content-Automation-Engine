from pydantic import BaseModel, Field


class FacebookStoryPost(BaseModel):
    title: str = Field(
        description="A short title identifying the curiosity/mystery (e.g. 'La Puerta al Infierno de Darvaza', 'Las Bóvedas de Semillas de Svalbard', 'El Mecanismo de Anticitera')"
    )
    category_label: str = Field(
        description="A short 1-2 word category in uppercase for the top badge (e.g., 'ARQUEOLOGÍA', 'COSMOS', 'MISTERIO', 'CIENCIA', 'GEOLOGÍA', 'ENIGMA')"
    )
    headline: str = Field(
        description=(
            "A high-impact, shocking headline question or hook for the story in Spanish, all in uppercase. "
            "Limit to 8-15 words. "
            "CRITICAL: Wrap the 2-4 most powerful words (verbs, key nouns, shocking adjectives) "
            "in square brackets so they will be rendered in glowing cyan/yellow. "
            "Example: '¿SABÍAS QUE [ESTA PUERTA] LLEVA [50 AÑOS ARDIENDO] SIN [APAGARSE NUNCA]?'"
        )
    )
    fact_text: str = Field(
        description=(
            "A concise, mind-blowing explanation of 25-40 words that answers the mystery or reveals the shocking fact. "
            "Clear, engaging, and easy to read quickly on a mobile screen."
        )
    )
    image_prompt: str = Field(
        description=(
            "A detailed prompt in English for Imagen 3/Vertex AI to generate a vertical (9:16 aspect ratio) cinematic, "
            "hyper-realistic, National Geographic style image of the mystery, structure, cosmic phenomenon, or ancient artifact. "
            "CRITICAL: The main subject must be centered in the upper 55% of the frame, leaving the bottom 45% relatively dark or simple "
            "so text overlay is completely legible. Do NOT include text, letters, watermarks, or borders."
        )
    )
