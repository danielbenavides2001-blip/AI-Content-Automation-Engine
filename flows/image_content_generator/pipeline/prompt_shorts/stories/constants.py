# Prompt constants for Curiosities Reels

IDEA_PROMPT_STORY = """
Genera una idea para un video corto (60 segundos) sobre "Curiosidades del Mundo" o "Datos Fascinantes".
El objetivo es educar pero de forma extremadamente entretenida, misteriosa o sorprendente (Ej: ¿Por qué los gatos ronronean? ¿Qué hay en el fondo de la Fosa de las Marianas? ¿Por qué soñamos?).
El video debe tener de 5 a 6 escenas (planteamiento intrigante, desarrollo rápido, y un dato final que deje la boca abierta).

**ESTILO VISUAL OBLIGATORIO:**
Si se deben generar imágenes de IA como respaldo, aplica este estilo: "{visual_style}"
"""

IMAGE_INTERACTION_PROMPT = "" # Not used for stories right now

AUDIO_PROMPT = """
Usa un tono narrativo, educativo pero muy intrigante y dinámico. Como si fueras un experto revelando un gran secreto del universo o de la historia.

TEXTO A NARRAR:
{audio_text}
"""


SCRIPT_PROMPT = """
Basándote en la IDEA proporcionada, escribe un guion de video para un Reel de 60 segundos.
Divide la historia en 5 o 6 escenas. Cada escena debe tener una narración en español, un prompt de imagen en inglés, y MUY IMPORTANTE: un `pexels_query` en inglés.

REGLAS CRÍTICAS:
1. El narrador debe sonar como un experto revelando un secreto fascinante.
2. La Escena 1 debe ser un gancho brutal (una pregunta o afirmación extraña) que impida hacer scroll.
3. El `intrigue_header` debe ser una frase de 3-5 palabras en MAYÚSCULAS que genere una curiosidad extrema (Ej: "EL SECRETO DE LOS GATOS", "¿POR QUÉ SOÑAMOS?").
4. El `pexels_query` debe ser de 1 a 3 palabras exactas en INGLÉS para buscar un video de stock en Pexels que encaje con la escena (Ej: 'cat sleeping', 'ocean waves', 'brain neurons').
5. Mantén el estilo visual solicitado en los prompts de imagen (por si falla la búsqueda de video).
"""

