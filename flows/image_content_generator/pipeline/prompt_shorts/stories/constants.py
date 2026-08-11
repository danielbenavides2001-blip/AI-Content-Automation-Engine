# Prompt constants for Curiosities Reels

IDEA_PROMPT_STORY = """
Genera una idea para un video corto viral sobre un dato curioso, misterio o historia fascinante.
El tema debe ser **EXTREMADAMENTE ESPECÍFICO, SORPRENDENTE Y POCO CONOCIDO** (algo que haga que la gente diga "no sabía eso" y quiera compartirlo).
El lenguaje debe ser **SUMAMENTE CLARO, DIRECTO Y FÁCIL DE ENTENDER** por cualquier persona al primer instante.
El video debe explicar todo el concepto de principio a fin, con un **GANCHO INICIAL BRUTAL** que impida hacer scroll, un desarrollo muy descriptivo y fácil de asimilar, y una **CONCLUSIÓN CERRADA** que resuelva la duda por completo.
Debe estar pensado para un video fluido, de ritmo rápido, compuesto por **6 a 8 escenas cortas** para mantener el dinamismo visual.
La narración completa de TODAS las escenas sumadas debe tener entre 130 y 180 palabras para que dure entre 50 y 75 segundos.
Máxima prioridad: **RETENCIÓN**. Cada segundo debe enganchar más que el anterior.

**POLÍTICA DE SEGURIDAD (BRAND SAFETY FACEBOOK):**
El tema debe ser **100% APTO PARA TODO PÚBLICO**. Está estrictamente prohibido generar ideas que involucren sangre, gore, muertes explícitas, violencia, tragedias gráficas o cualquier contenido que viole las políticas de Facebook/Instagram. Mantén un enfoque de asombro científico, educativo y respetuoso.

**ESTILO VISUAL OBLIGATORIO:**
Si se deben generar imágenes de IA como respaldo, aplica este estilo: "{visual_style}"
"""

IMAGE_INTERACTION_PROMPT = "" # Not used for stories right now

AUDIO_PROMPT = """
Usa un tono narrativo intrigante, dinámico y con energía. Como si estuvieras contando un secreto alucinante a un amigo. Mantén ritmo rápido, sin pausas largas.

TEXTO A NARRAR:
{audio_text}
"""


SCRIPT_PROMPT = """
Basándote en la IDEA proporcionada, escribe un guion de video para un Reel que dure entre 50 y 75 segundos.
Divide la historia en **6 a 8 escenas cortas** (alta densidad visual, cambios rápidos de clip).
Para cada escena debes definir:
1. `visual_type`: Escoge `"stock_video"` si es algo común que se puede grabar en la vida real (ej: gente caminando, cielo, ciudad, naturaleza). Escoge `"ai_image"` si es algo abstracto, fantástico, histórico, científico o imposible de capturar (ej: neuronas, ADN, concepto abstracto, criatura rara).
2. `pexels_query`: Solo si elegiste "stock_video", escribe 1 a 3 palabras clave EN INGLÉS.
3. `image_prompt`: La descripción detallada EN INGLÉS. **CRÍTICO:** Debe describir literalmente la acción, el misterio, el artefacto antiguo o la cultura específica mencionada en la narración. Usa detalles visuales hiperrealistas y de estructura viral (ej: 'ancient golden artifact glowing in a dark cave, hyper-realistic, cinematic lighting, national geographic photography'). **PROHIBIDO** usar descripciones genéricas o arte abstracto. El enfoque visual debe atrapar al espectador desde el primer segundo mostrando algo fascinante y visualmente asombroso.
4. `narration`: Lo que dirá el locutor.

REGLAS CRÍTICAS DE RETENCIÓN:
1. **GANCHO MORTAL:** La Escena 1 debe ser una pregunta impactante, un dato que rompa la mente o una afirmación tan increíble que sea imposible hacer scroll. Ej: "¿Sabías que tu cerebro toma decisiones 7 segundos ANTES de que tú seas consciente?"
2. **RITMO ACELERADO:** Cada escena debe durar máximo 5-7 segundos. Cambios rápidos. Sin tiempos muertos.
3. **CURIOSIDAD CONSTANTE:** Cada escena debe revelar una capa nueva de información que mantenga la intriga. Estructura: Gancho → Explicación → Revelación → Cierre.
4. **LÍMITE DE PALABRAS:** La narración total de todo el video debe tener entre **130 y 180 palabras**. Esto asegura una duración de 50-75 segundos para calificar a anuncios mid-roll.
5. **CLARIDAD ABSOLUTA:** Explica el dato de forma sumamente sencilla y comprensible. El espectador debe entenderlo al instante. Evita tecnicismos y metáforas confusas.
6. **HISTORIA COMPLETA:** La explicación debe quedar 100% resuelta en la última escena. No dejes cabos sueltos.
7. El `intrigue_header` debe ser un título de 3-5 palabras en MAYÚSCULAS que genere intriga inmediata (Ej: "EL PODER OCULTO", "NO VAS A CREER", "TU CEREBRO MIENTE").
8. **LLAMADO A LA ACCIÓN (CTA):** En la última escena, incluye un CTA interactivo que invite a comentar (Ej: "¿Conocías este dato? Te leo en los comentarios").
9. **SEGURO PARA FACEBOOK (BRAND SAFETY):** Todo el guion, descripciones de imágenes y textos deben ser 100% aptos para todo público. **PROHIBIDO** incluir descripciones de sangre, gore, violencia, cadáveres, destrucción masiva gráfica o lenguaje que pueda causar un baneo en redes sociales.
"""
