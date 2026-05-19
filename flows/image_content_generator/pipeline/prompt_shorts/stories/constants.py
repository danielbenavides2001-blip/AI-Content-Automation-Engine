# Prompt constants for Curiosities Reels

IDEA_PROMPT_STORY = """
Genera una idea para un video corto sobre "Curiosidades e Historias Insólitas de Civilizaciones Antiguas".
El tema debe ser **EXTREMADAMENTE ESPECÍFICO, CURIOSO Y POCO CONOCIDO** (datos insólitos o secretos que casi nadie sabe que ocurrieron en el pasado).
El lenguaje debe ser **SUMAMENTE CLARO, DIRECTO Y FÁCIL DE ENTENDER** por cualquier persona al primer instante.
El video debe explicar todo el concepto de principio a fin, con un inicio intrigante, un desarrollo muy descriptivo y fácil de asimilar, y una **CONCLUSIÓN CERRADA** que resuelva la duda por completo (sin dejar la historia a medias).
Debe estar pensado para un video fluido, de ritmo rápido, compuesto por **6 a 8 escenas cortas** para mantener el dinamismo visual.
La narración completa de TODAS las escenas sumadas NO DEBE SUPERAR LAS 120 PALABRAS para que dure menos de 60 segundos.

**ESTILO VISUAL OBLIGATORIO:**
Si se deben generar imágenes de IA como respaldo, aplica este estilo: "{visual_style}"
"""

IMAGE_INTERACTION_PROMPT = "" # Not used for stories right now

AUDIO_PROMPT = """
Usa un tono narrativo, educativo pero muy intrigante y dinámico. Como si fueras un experto revelando un gran secreto de la historia antigua.

TEXTO A NARRAR:
{audio_text}
"""


SCRIPT_PROMPT = """
Basándote en la IDEA proporcionada, escribe un guion de video para un Reel que dure MÁXIMO 50 segundos.
Divide la historia en **6 a 8 escenas cortas** (alta densidad visual, cambios rápidos de clip).
Para cada escena debes definir:
1. `visual_type`: Escoge `"stock_video"` si es algo común que se puede grabar en la vida real (ej: arena del desierto, fuego, gente sonriendo). Escoge `"ai_image"` si es histórico, fantasioso o imposible de capturar (ej: gladiadores romanos peleando, médicos egipcios, un templo maya).
2. `pexels_query`: Solo si elegiste "stock_video", escribe 1 a 3 palabras clave EN INGLÉS.
3. `image_prompt`: La descripción detallada EN INGLÉS (siempre obligatoria como respaldo).
4. `narration`: Lo que dirá el locutor.

REGLAS CRÍTICAS:
1. **CRITERIO VISUAL:** Sé muy inteligente decidiendo el `visual_type`. Para todo lo que requiera ver ejércitos, vestimenta de la época, reyes antiguos o monumentos en su esplendor, usa "ai_image".
2. **LÍMITE ESTRICTO DE TIEMPO:** La narración total de Todo el video sumado debe tener **máximo 120 palabras**. Escribe de forma resumida, directa al grano, sin rodeos.
3. **CLARIDAD ABSOLUTA:** Explica la curiosidad de forma sumamente sencilla y comprensible. El espectador debe entender al instante el contexto de la época, qué ocurría y por qué se hacía. Evita metáforas confusas.
4. **HISTORIA COMPLETA:** La explicación debe quedar 100% resuelta en la última escena.
5. La Escena 1 debe ser un gancho brutal (una pregunta muy específica o dato impactante) sobre la civilización que impida hacer scroll.
6. El `intrigue_header` debe ser el título persistente de 3-5 palabras en MAYÚSCULAS (Ej: "EL IMPUESTO ROMANO", "SECRETOS DE EGIPTO").
7. **LLAMADO A LA ACCIÓN (CTA):** En la última escena, incluye un CTA interactivo sencillo (Ej: "¿Conocías este dato? Cuéntanos en los comentarios").
"""
