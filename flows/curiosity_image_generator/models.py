from pydantic import BaseModel, Field

class CuriosityPost(BaseModel):
    title: str = Field(description="A short title for the curiosity (e.g. 'El Saltamontes Rosa')")
    caption: str = Field(
        description=(
            "An engaging, viral Facebook post caption in Spanish. "
            "It must start with a hook, contain the detailed curious story, "
            "use relevant emojis, include hashtags (e.g., #EnigmaIQ, #curiosidades), "
            "and end with an interactive question to drive comments."
        )
    )
    image_prompt: str = Field(
        description=(
            "A detailed prompt for Imagen 3/Vertex AI to generate a photorealistic representation of the curiosity. "
            "It should describe the subject, texture, dramatic lighting (e.g., warm side-lighting, dark slate background), "
            "cinematic shot, and specify an aspect ratio of '1:1' (square) or '4:5' for optimal Facebook feed display. "
            "Do NOT include text inside the image."
        )
    )
