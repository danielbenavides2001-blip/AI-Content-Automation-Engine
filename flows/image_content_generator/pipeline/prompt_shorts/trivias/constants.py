# Prompts and constants for Curiosity Reels

IDEA_PROMPT_TRIVIAS = """
Genera una idea altamente viral y adictiva para un video de curiosidades corto (Reel/Short).
El tema debe ser **FASCINANTE, DIVERTIDO Y SORPRENDENTE**. Las curiosidades pueden abarcar cualquier área del conocimiento:
- **Ciencia y Naturaleza**: Datos alucinantes sobre el cuerpo humano, el espacio, los animales, la física o la biología.
- **Cultura General**: Hechos insólitos sobre historia, geografía, tecnología, arte, psicología o lenguaje.
- **Vida Cotidiana**: El origen secreto de cosas que usas a diario, mitos que la ciencia desmintió, récords extremos.

El video debe estructurarse como un reto interactivo con las siguientes partes:
1. **Intro corta (Escena 1)**: Un gancho brutal que desafíe al usuario a demostrar cuánto sabe (Ej: "Solo el 5% logra acertar estas 5 preguntas... ¿Eres uno de ellos? ¡Vamos a ver!").
2. **Desarrollo (Escenas 2 a 6)**: 5 preguntas de curiosidades diseñadas para asombrar y mantener al espectador pegado a la pantalla.
3. **Outro corta (Escena 7)**: Llamado a la acción agresivo invitando al usuario a comentar cuántas acertó y a seguir el canal para más curiosidades.

La narración completa del video debe ser ultra directa y fluida, optimizada para durar entre 45 y 75 segundos.

**ESTILO VISUAL RECOMENDADO PARA LAS IMÁGENES/VIDEOS DE FONDO:**
Aplica este estilo cinematográfico de soporte: "{visual_style}"
"""

SCRIPT_PROMPT_TRIVIAS = """
Basándote en la IDEA de curiosidad proporcionada, escribe un guion de video estructurado y dinámico para un Reel de curiosidades.
Divide el video en **exactamente 7 escenas**:
- Escena 1: Introducción (Sin pregunta, solo gancho inicial).
- Escena 2: Pregunta/Curiosidad 1.
- Escena 3: Pregunta/Curiosidad 2.
- Escena 4: Pregunta/Curiosidad 3.
- Escena 5: Pregunta/Curiosidad 4.
- Escena 6: Pregunta/Curiosidad 5.
- Escena 7: Conclusión/Outro (Sin pregunta, solo llamado a la acción).

Para cada escena debes definir en JSON:
1. `scene_number`: Número secuencial (1 a 7).
2. `question`: El texto de la pregunta que aparecerá en pantalla. (Vacío en Escenas 1 y 7).
3. `options`: Lista de exactamente 4 opciones de respuesta formateadas como "A) Opción 1", "B) Opción 2", "C) Opción 3", "D) Opción 4". (Vacío en Escenas 1 y 7).
4. `correct_answer`: La opción correcta exactamente igual a como aparece en la lista (Ej: "B) Opción 2"). (Vacío en Escenas 1 y 7).
5. `narration_question`: Lo que dirá la voz al inicio de la escena planteando la pregunta con tono entusiasta e intrigante. En Escenas 1 y 7, pon aquí la narración estándar del gancho/despedida.
6. `narration_answer`: Lo que dirá la voz después de que pasen los 2 segundos del temporizador, revelando y explicando brevemente la respuesta correcta de forma gratificante e informativa (Ej: "¡Exacto! Es el pulpo, el animal con tres corazones."). (Vacío en Escenas 1 y 7).
7. `visual_type`: Escoge `"stock_video"` (para clips en movimiento relacionados de fondo como naturaleza, ciencia, espacio, etc.) o `"ai_image"` (para recreaciones específicas generadas por IA si no hay video obvio).
8. `pexels_query`: Si elegiste `"stock_video"`, escribe 1 a 3 palabras clave EN INGLÉS que coincidan perfectamente con la temática de la escena (Ej: 'brain anatomy', 'space nebula galaxy', 'ocean waves'). Deja vacío en caso contrario.
9. `image_prompt`: La descripción física muy detallada EN INGLÉS del estilo visual que debe tener la imagen de respaldo (siempre obligatoria, respetando la guía de estilo recomendada).
10. `sfx`: Sonido de impacto ambiental o transición para esta escena (escoge entre: 'digital_swoosh', 'ocean_waves', 'jungle_ambient', 'none').

REGLAS CRÍTICAS DE REDACCIÓN:
1. **LÍMITE ESTRICTO DE PALABRAS:** La suma total de palabras en todo el guion no debe exceder las 200 palabras. Esto asegura una duración de video entre 50 y 75 segundos.
2. **OPCIONES LEGIBLES:** Asegúrate de que las opciones sean cortas, precisas y claramente distinguibles.
3. **INTRIGA CONSTANTE:** Mantén un tono sumamente interactivo, como si estuvieras desafiando personalmente al espectador cara a cara.
4. **OUTRO:** Pide explícitamente al espectador que escriba en los comentarios su puntaje final: "¿Cuántas acertaste? Escríbelo en los comentarios".
"""

FOCUS_AREAS_TRIVIAS = [
    "CURIOSIDADES DE CIENCIA Y ESPACIO: Datos alucinantes sobre el cosmos, el cuerpo humano, la física cuántica o descubrimientos científicos recientes.",
    "CURIOSIDADES DE HISTORIA OCULTA: Hechos sorprendentes de la historia que no enseñan en la escuela, mitologías antiguas o civilizaciones perdidas.",
    "CURIOSIDADES DEL MUNDO ANIMAL: Habilidades increíbles de animales, comportamientos extraños, records de supervivencia y criaturas fascinantes.",
    "CURIOSIDADES DE LA NATURALEZA Y GEOGRAFÍA: Fenómenos naturales que parecen magia, lugares extremos, fronteras absurdas y misterios geográficos.",
    "CURIOSIDADES DE PSICOLOGÍA Y COMPORTAMIENTO: Sesgos cognitivos, por qué hacemos lo que hacemos, trampas mentales y el poder del inconsciente.",
    "CURIOSIDADES DE TECNOLOGÍA E INVENTOS: Inventos accidentales que cambiaron el mundo, tecnología que parece ciencia ficción y secretos de internet.",
    "CURIOSIDADES DEL LENGUAJE Y LA CULTURA: Palabras fascinantes, el origen de expresiones cotidianas, símbolos ocultos y datos lingüísticos sorprendentes.",
    "CURIOSIDADES DE LA VIDA COTIDIANA: El origen secreto de objetos comunes, mitos desmentidos por la ciencia y datos que cambiarán cómo ves el mundo.",
    "CURIOSIDADES DE RÉCORDS Y EXTREMOS: Las marcas más insólitas, casos extremos de resistencia humana y objetos/lugares con récords imposibles.",
    "CURIOSIDADES DE ALIMENTACIÓN: La ciencia detrás de tus comidas favoritas, historia oculta de los alimentos y mitos alimenticios desmentidos."
]
