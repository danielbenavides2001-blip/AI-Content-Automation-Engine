from pydantic import BaseModel, Field

class CuriosityPost(BaseModel):
    title: str = Field(description="A short title for the curiosity (e.g. 'El Mecanismo de Anticitera', 'El Ojo del Sahara', 'Las Bóvedas de Svalbard')")
    headline: str = Field(
        description=(
            "A high-impact news headline in Spanish, all in uppercase. "
            "It must describe the curious fact in a shocking or dramatic way. "
            "Limit to 10-18 words. "
            "CRITICAL: Wrap the 2-4 most important keywords (verbs, nouns, adjectives) "
            "that should be highlighted in cian in square brackets. "
            "Example: 'ARQUEÓLOGOS [HALLAN] UNA MISTERIOSA [ESTRUCTURA] SUMERGIDA EN EL [TRIÁNGULO DE LAS BERMUDAS].'"
        )
    )
    caption: str = Field(
        description=(
            "An engaging, viral Facebook post caption in Spanish. "
            "It must start with a hook, contain the detailed curious story, "
            "use relevant emojis, include hashtags (e.g., #EnigmaIQ, #curiosidades, #misterios, #historia), "
            "and end with an interactive question to drive comments. "
            "Strictly brand safe (no gore, no violence, no death)."
        )
    )
    image_prompt: str = Field(
        description=(
            "A detailed prompt for Imagen 3/Vertex AI in English to generate a photorealistic representation of the curiosity. "
            "Specify an aspect ratio of '4:5' (vertical). "
            "CRITICAL: Instruct that the main subject (ancient structure, artifact, cosmic anomaly, bizarre geological place) "
            "must be located in the top 60% of the frame, leaving the bottom 40% clear or empty (e.g. blurred background, ground, simple texture) "
            "so that we can overlay text without blocking the main subject. "
            "Hyper-realistic, cinematic lighting, national geographic style, 8k resolution. "
            "Do NOT include text or watermarks inside the image."
        )
    )
