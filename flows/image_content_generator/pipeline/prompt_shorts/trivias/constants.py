# Prompts and constants for Trivia Reels

IDEA_PROMPT_TRIVIAS = """
Genera una idea altamente viral y adictiva para un video de trivia corto (Reel/Short).
El tema debe ser **FASCINANTE, DIVERTIDO Y EXTREMADAMENTE DESAFIANTE**. Las trivias pueden abarcar cualquier área del conocimiento:
- **Ortografía y Gramática**: ¿Cómo se escribe correctamente esta palabra?, ¿Cuál es el significado real de este término?, ¿Cuál es el sinónimo de...?
- **Cultura General**: Datos curiosos e insólitos sobre ciencia, espacio, geografía, historia, mitología, cine, música o deportes.
- **Fútbol Mundial**: Records legendarios, mundiales históricos, datos asombrosos sobre jugadores míticos.

El video debe estructurarse como un juego de preguntas interactivo con las siguientes partes:
1. **Intro corta (Escena 1)**: Un gancho brutal que desafíe al usuario a poner a prueba su cerebro (Ej: "Solo el 5% logra responder estas 4 preguntas... ¿Eres uno de ellos? ¡Vamos a ver!").
2. **Desarrollo (Escenas 2 a 5)**: 4 preguntas de trivia diseñadas para asombrar y mantener al espectador pegado a la pantalla.
3. **Outro corta (Escena 6)**: Llamado a la acción agresivo invitando al usuario a comentar cuántas preguntas respondió correctamente y a seguir el canal para el desafío de mañana.

La narración completa del video debe ser ultra directa y fluida, optimizada para durar menos de 60 segundos.

**ESTILO VISUAL RECOMENDADO PARA LAS IMÁGENES/VIDEOS DE FONDO:**
Aplica este estilo cinematográfico de soporte: "{visual_style}"
"""

SCRIPT_PROMPT_TRIVIAS = """
Basándote en la IDEA de trivia proporcionada, escribe un guion de video estructurado y dinámico para un Reel de trivia.
Divide el video en **exactamente 6 escenas**:
- Escena 1: Introducción (Sin pregunta de trivia, solo gancho inicial).
- Escena 2: Pregunta 1.
- Escena 3: Pregunta 2.
- Escena 4: Pregunta 3.
- Escena 5: Pregunta 4.
- Escena 6: Conclusión/Outro (Sin pregunta de trivia, solo llamado a la acción).

Para cada escena debes definir en JSON:
1. `scene_number`: Número secuencial (1 a 6).
2. `question`: El texto de la pregunta que aparecerá en pantalla. (Vacío en Escenas 1 y 6).
3. `options`: Lista de exactamente 4 opciones de respuesta formateadas como "A) Opción 1", "B) Opción 2", "C) Opción 3", "D) Opción 4". (Vacío en Escenas 1 y 6).
4. `correct_answer`: La opción correcta exactamente igual a como aparece en la lista (Ej: "B) Opción 2"). (Vacío en Escenas 1 y 6).
5. `narration_question`: Lo que dirá la voz al inicio de la escena planteando la pregunta con tono entusiasta e intrigante. En Escenas 1 y 6, pon aquí la narración estándar del gancho/despedida.
6. `narration_answer`: Lo que dirá la voz después de que pasen los 3 segundos del temporizador, revelando y explicando brevemente la respuesta correcta de forma gratificante e informativa (Ej: "¡Exacto! Es París, la llamada Ciudad de la Luz."). (Vacío en Escenas 1 y 6).
7. `visual_type`: Escoge `"stock_video"` (para clips en movimiento relacionados de fondo como planetas, estadios, libros, etc.) o `"ai_image"` (para recreaciones específicas generadas por IA si no hay video obvio).
8. `pexels_query`: Si elegiste `"stock_video"`, escribe 1 a 3 palabras clave EN INGLÉS que coincidan perfectamente con la temática de la escena (Ej: 'spelling book drone', 'football stadium lights', 'space planet galaxy'). Deja vacío en caso contrario.
9. `image_prompt`: La descripción física muy detallada EN INGLÉS del estilo visual que debe tener la imagen de respaldo (siempre obligatoria, respetando la guía de estilo recomendada).
10. `sfx`: Sonido de impacto ambiental o transición para esta escena (escoge entre: 'digital_swoosh', 'ocean_waves', 'jungle_ambient', 'none').

REGLAS CRÍTICAS DE REDACCIÓN:
1. **LÍMITE ESTRICTO DE PALABRAS:** Mantén la locución de cada escena concisa y directa al grano. La suma total de palabras en todo el guion no debe exceder las 140 palabras para mantener un ritmo dinámico e hiperactivo.
2. **OPCIONES LEGIBLES:** Asegúrate de que las opciones sean cortas, precisas y claramente distinguibles.
3. **INTRIGA CONSTANTE:** Mantén un tono sumamente interactivo, como si estuvieras desafiando personalmente al espectador cara a cara.
4. **OUTRO:** Pide explícitamente al espectador que escriba en los comentarios su puntaje final: "¿Cuántas acertaste? Escríbelo en los comentarios".
"""

FOCUS_AREAS_TRIVIAS = [
    "TRIVIA DE ORTOGRAFÍA Y GRAMÁTICA: Desafíos sobre palabras difíciles de escribir (como por qué, porque, porqué, cónyuge, idiosincrasia), sinónimos insólitos y trampas lingüísticas.",
    "TRIVIA DE FÚTBOL MUNDIAL: Preguntas sobre mundiales, records de goleadores, datos locos sobre leyendas como Maradona, Pelé, Messi y estadios legendarios.",
    "TRIVIA DE CURIOSIDADES DEL ESPACIO Y CIENCIA: Misterios de los planetas, física loca, el cuerpo humano, células, virus y descubrimientos científicos asombrosos.",
    "TRIVIA DE HISTORIA OCULTA Y MITOLOGÍA: Secretos de emperadores romanos, batallas absurdas de la historia, dioses griegos y leyendas antiguas.",
    "TRIVIA DE GEOGRAFÍA EXTREMA Y FRONTERAS: Preguntas sobre los países más pequeños, fronteras absurdas, islas misteriosas y capitales que confunden a todo el mundo.",
    "TRIVIA DE SIGNIFICADOS Y PALABRAS FASCINANTES: ¿Qué significa 'serendípia', 'petricor', 'epifanía'? Preguntas interactivas sobre el vocabulario más hermoso del español.",
    "TRIVIA DE ANIMALES EXTRAÑOS Y REINO SALVAJE: Habilidades locas de criaturas marinas, insectos brutales y mamíferos con records de supervivencia."
]
