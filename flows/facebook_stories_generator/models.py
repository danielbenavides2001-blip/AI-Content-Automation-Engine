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
            "A short, shocking headline question or hook for the story in Spanish, all in uppercase. "
            "STRICT LIMIT: 8 to 12 words only! Do not write long paragraphs. "
            "CRITICAL: Wrap the 2-3 most powerful words in square brackets for neon highlight. "
            "Example: '¿SABÍAS QUE [ESTA PUERTA] LLEVA [50 AÑOS ARDIENDO] SIN [APAGARSE]?'"
        )
    )
    fact_text: str = Field(
        description=(
            "A short, concise explanation of 15 to 22 words that answers the mystery or reveals the shocking fact. "
            "Extremely easy to read in 3 seconds on a mobile screen."
        )
    )
    post_caption: str = Field(
        description=(
            "An engaging, viral Facebook feed caption in Spanish for when this image is published as a regular post. "
            "It must start with an attention-grabbing hook, explain the fascinating story in detail (2-3 short paragraphs), "
            "use relevant emojis, include hashtags (e.g. #EnigmaIQ, #curiosidades, #misterios, #historia), "
            "and end with an interactive question to drive comments. "
            "Strictly brand safe (no gore, no violence, no death)."
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
