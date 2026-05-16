# Prompt constants for Curiosities Reels

IDEA_PROMPT_STORY = """
Genera una idea para un video corto sobre "Curiosidades del Mundo".
El tema debe ser **EXTREMADAMENTE ESPECÍFICO Y COTIDIANO**, respondiendo a una pregunta concreta (Ej: "¿Por qué los gatos ronronean?", "¿Por qué las venas se ven azules si la sangre es roja?").
El video debe tener un guion que explique todo el concepto de principio a fin, con un inicio, desarrollo y una **CONCLUSIÓN CERRADA** (no dejes la historia a medias o cortada).
Debe estar pensado para un video fluido, de ritmo rápido, compuesto por **6 a 8 escenas cortas** para que visualmente nunca se sienta estancado.
La narración completa de TODAS las escenas sumadas NO DEBE SUPERAR LAS 120 PALABRAS, para garantizar que el video dure menos de 60 segundos.

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
Basándote en la IDEA proporcionada, escribe un guion de video para un Reel que dure MÁXIMO 50 segundos.
Divide la historia en **6 a 8 escenas cortas** (alta densidad visual, cambios rápidos de clip).
Cada escena debe tener una narración en español, un prompt de imagen en inglés, y MUY IMPORTANTE: un `pexels_query` en inglés.

REGLAS CRÍTICAS:
1. **LÍMITE ESTRICTO DE TIEMPO:** La narración total de TODO el video sumado debe tener **máximo 120 palabras**. Escribe de forma muy resumida, directa al grano, sin pausas largas ni rodeos.
2. **HISTORIA COMPLETA:** La explicación debe quedar 100% terminada y resuelta en la última escena. NUNCA la dejes cortada ni termines abruptamente.
3. El narrador debe sonar fluido, dinámico y amigable, revelando el dato como algo fascinante.
4. La Escena 1 debe ser un gancho brutal (una pregunta muy específica) que impida hacer scroll.
5. El `intrigue_header` debe ser el título persistente de 3-5 palabras en MAYÚSCULAS (Ej: "¿POR QUÉ RONRONEAN?", "EL SECRETO DE LAS VENAS").
6. **VARIEDAD VISUAL:** El `pexels_query` debe ser de 1 a 3 palabras exactas en INGLÉS. Como tienes 6-8 escenas, asegúrate de que **CADA escena tenga un query visualmente diferente** para que el video sea muy fluido y no se repitan los mismos planos de fondo.
"""

