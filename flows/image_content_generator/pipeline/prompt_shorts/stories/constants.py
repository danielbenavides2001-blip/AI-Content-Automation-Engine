# Prompt constants for Story Reels

IDEA_PROMPT_STORY = """
Genera una idea para un video corto (60 segundos) sobre una historia atrapante, misteriosa, o dramática.
Puede ser al estilo "Reddit" (historia anónima de traición/éxito), un misterio histórico poco conocido, o un true-crime rápido.
El video debe tener de 5 a 6 escenas (planteamiento, nudo, clímax, y un plot-twist al final).

**ESTILO VISUAL OBLIGATORIO:**
Aplica este estilo a todas las imágenes: "{visual_style}"
"""

IMAGE_INTERACTION_PROMPT = "" # Not used for stories right now

AUDIO_PROMPT = """
Usa un tono narrativo, de suspenso, intrigante y ligeramente dramático. Como si estuvieras contando un secreto oscuro o un chisme muy grave.
"""

SCRIPT_PROMPT = """
Basándote en la IDEA proporcionada, escribe un guion de video para un Reel de 60 segundos.
Divide la historia en 5 o 6 escenas. Cada escena debe tener una narración en español y un prompt de imagen detallado en inglés.

REGLAS CRÍTICAS:
1. El narrador debe mantener el suspenso. 
2. La Escena 1 debe ser un gancho brutal que impida hacer scroll.
3. El `intrigue_header` debe ser una frase de 3-5 palabras en MAYÚSCULAS que genere una curiosidad extrema (Ej: "EL SECRETO DEL MILLONARIO", "NO CREERÁS EL FINAL").
4. Mantén el estilo visual solicitado en todos los prompts de imagen.
"""

