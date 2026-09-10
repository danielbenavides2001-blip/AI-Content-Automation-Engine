# Prompt constants for Curiosities Reels

IDEA_PROMPT_STORY = """
Genera una idea para un video corto viral (Reel/Short/TikTok) sobre un misterio fascinante, criatura extrema, fenómeno inexplicable o secreto histórico.
El tema debe ser **EXTREMADAMENTE ESPECÍFICO, SORPRENDENTE Y POCO CONOCIDO** (algo que obligue al espectador a quedarse para saber el desenlace).
El lenguaje debe ser **SUMAMENTE DIRECTO, DINÁMICO Y FÁCIL DE ENTENDER** para cualquier persona desde el primer instante.

**ESTRUCTURA DE RETENCIÓN EXTREMA:**
- **GANCHO INICIAL DE IMPACTO (Primeros 3 segundos):** Debe romper el scroll al instante con una afirmación contundente, un misterio no resuelto o un descubrimiento insólito.
- **RITMO ACELERADO:** Diseñado para **7 a 9 escenas cortas** (cambio visual constante cada 4 a 6 segundos).
- **DESARROLLO FASCINANTE:** Cada escena revela una capa nueva de misterio o dato concreto, manteniendo la intriga en aumento constante.
- **DESENLACE SATISFACTORIO:** Resuelve el enigma con claridad y remata con una pregunta que invite a debatir en los comentarios.

La narración completa de TODAS las escenas sumadas debe tener entre **140 y 180 palabras** para que dure entre 55 y 65 segundos (duración óptima de retención y monetización).

**POLÍTICA DE SEGURIDAD (BRAND SAFETY FACEBOOK):**
El tema debe ser **100% APTO PARA TODO PÚBLICO**. Está estrictamente prohibido generar ideas que involucren sangre, gore, muertes explícitas, violencia, tragedias gráficas o cualquier contenido que viole las políticas de Facebook/Instagram. Mantén un enfoque de asombro científico, educativo y respetuoso.

**ESTILO VISUAL OBLIGATORIO:**
Si se deben generar imágenes de IA como respaldo, aplica este estilo: "{visual_style}"
"""

IMAGE_INTERACTION_PROMPT = "" # Not used for stories right now

AUDIO_PROMPT = """
Usa un tono narrativo intrigante, cinematográfico y lleno de energía. Como si estuvieras revelando un secreto alucinante que nadie más conoce. Mantén un ritmo ágil, seguro y fluido, sin pausas innecesarias.

TEXTO A NARRAR:
{audio_text}
"""


SCRIPT_PROMPT = """
Basándote en la IDEA proporcionada, escribe un guion de video para un Reel que dure entre 55 y 65 segundos.
Divide la historia en **7 a 9 escenas cortas** (máxima densidad visual, cambios rápidos de plano cada 4-6 segundos).

Para cada escena debes definir:
1. `visual_type`: Escoge `"stock_video"` si es algo común de la vida real (ej: océano, cielo, arqueólogo excavando, ciudad, microscopio). Escoge `"ai_image"` si es algo fantástico, histórico, prehistórico, criatura insólita, artefacto milenario o fenómeno invisible a simple vista.
2. `pexels_query`: Solo si elegiste "stock_video", escribe 1 a 3 palabras clave precisas EN INGLÉS.
3. `image_prompt`: La descripción detallada EN INGLÉS. **CRÍTICO:** Debe describir con enorme fuerza visual la acción, criatura o artefacto de la escena. Usa iluminación cinematográfica, texturas hiperrealistas y encuadres dramáticos (ej: 'ancient colossal megalith discovered under deep ocean, glowing bioluminescent particles, national geographic photography, 8k resolution, cinematic lighting'). **PROHIBIDO** descripciones abstractas o aburridas.
4. `narration`: Lo que dirá el locutor.

REGLAS DE ORO DE VIRALIDAD Y RETENCIÓN (2026):
1. ⚡ **GANCHO SCROLL-STOPPER (Escena 1):**
   - **PROHIBIDO INICIAR CON:** "¿Sabías que...?", "¿Alguna vez te has preguntado...?", "¿Te imaginas si...?", "Hoy te voy a contar...", "En el vasto mundo...", "Bienvenidos...", "Imagina un lugar...".
   - **OBLIGATORIO:** La primera frase debe ser una bomba de curiosidad directa, una advertencia o una anomalía que rompa la lógica.
   - Ejemplos de ganchos ganadores:
     * "Científicos acaban de encontrar algo en las profundidades del océano que no debería existir."
     * "Este artefacto de 2.000 años contiene una tecnología que los ingenieros todavía no logran descifrar."
     * "Si alguna vez ves esta extraña marca en una roca antigua, aléjate de inmediato."
     * "Hay una razón por la que este sitio fue borrado de todos los mapas oficiales del planeta."
2. ⏩ **RITMO RÁPIDO Y FLUIDO:** Cada escena debe tener entre 18 y 25 palabras (4 a 6 segundos). Cero rodeos, cero explicaciones aburridas.
3. 🧩 **CURIOSITY GAP (Bucle de curiosidad constante):** Cada escena debe abrir una nueva interrogante o revelar una pista sorprendente. Estructura: Gancho impactante → El enigma inexplicable → La pista oculta → La revelación científica/histórica → Cierre y debate.
4. 📏 **LÍMITE TOTAL DE PALABRAS:** Entre **140 y 180 palabras** en total para todo el guion (55-65 segundos).
5. 🏷️ **INTRIGUE HEADER:** Frase corta de 3-5 palabras en MAYÚSCULAS para la parte superior de la pantalla (ej: "MISTERIO DESCLASIFICADO", "NO DEBERÍA EXISTIR", "ANOMALÍA HISTÓRICA").
6. 💬 **LLAMADO A LA ACCIÓN (CTA QUE DETONA COMENTARIOS):** En la última escena, remata con una pregunta provocadora para que la gente debata sus teorías en comentarios (ej: "¿Crees que fue obra humana o algo que aún no comprendemos? Déjame tu teoría abajo 👇").
7. 🛡️ **BRAND SAFETY FACEBOOK:** Contenido 100% apto para todo público. Sin violencia, sin sangre, sin temas morbosos. Puro asombro y fascinación.
"""
