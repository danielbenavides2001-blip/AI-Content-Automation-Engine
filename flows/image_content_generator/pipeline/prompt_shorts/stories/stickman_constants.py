from typing import ClassVar

IDEA_PROMPT_STICKMAN = """
ROL: Eres un experto en psicología conductual, guionista de cine negro y artista conceptual. Tu misión es generar de forma infinita contenido para videos impactantes de MÁXIMO 29 segundos divididos en 4 escenas visuales exactas.

1. MOTOR DE ORIGINALIDAD (Cero Repetición)
Para cada nuevo video, debes elegir un Eje Temático y un Símbolo Visual.
Ejes Temáticos disponibles: Autoengaño, Envidia, Ambición tóxica, Procrastinación, Duelo, Validación externa, Ego, Disciplina, Silencio, Intuición.
Símbolos Visuales Prohibidos de repetir (SI YA SE USARON): Hilos de títere, Mesas que se encogen, Sombrillas/Lluvia, Puertas de búnker, Espejos, Relojes de arena.

TEMA CENTRAL OBLIGATORIO: {selected_area}
ESTILO VISUAL: Estilo Noir, Minimalist 2D hand-drawn.

2. REGLAS DEL GUION (Narrativa Fluida y Atractiva)
El guion debe durar MÁXIMO 29 segundos. El texto debe ser fluido, evitar palabras rebuscadas y capturar la atención desde el primer segundo.
Escena 1 (Planteamiento del Dolor): Una observación sobre un comportamiento humano común pero dañino.
Escena 2 (El Juicio Externo): Cómo el mundo intenta mantenerte en ese comportamiento.
Escena 3 (El Acto de Ruptura): Una decisión interna o cambio de perspectiva.
Escena 4 (La Sabiduría Final): Una frase lapidaria que cierre con autoridad.
Tono de voz: Serio, pero ATRACTIVO, FLUIDO y con carga emocional sutil.

3. DIRECCIÓN DE ARTE (Prompts de Imagen para Video)
Cada video consta de 4 imágenes que se convertirán en video.
Estilo Visual Estricto: "Minimalist 2D hand-drawn animation, Noir aesthetic, extreme high contrast (Chiaroscuro), deep black shadows, cinematic lighting."
Personaje: "Stickman with a white circular head, expressive facial features, and a thin black body."
Paleta de Colores: Escala de grises. Solo se permite un Acento de Color (Dorado, Rojo o Azul Eléctrico) en la Escena 4 para resaltar el elemento de poder o paz.

INSTRUCCIONES DE MOVIMIENTO (Image-to-Video):
Para cada escena, define instrucciones de movimiento cortas y potentes (V1, V2, V3, V4).

HISTORIAL DE TEMAS A EVITAR:
{avoid_msg}

RESPONDE EXCLUSIVAMENTE EN FORMATO JSON siguiendo este esquema:
{{
  "title": "Título corto y potente",
  "hook": "Gancho de interrupción (10-15 palabras) para detener el scroll",
  "selected_theme": "El eje temático elegido",
  "selected_symbol": "El símbolo visual elegido",
  "scenes": [
    {{
      "scene_number": 1,
      "narration": "Texto fluido de aprox 6-7 segundos",
      "image_prompt": "Prompt en inglés siguiendo el estilo Noir",
      "movement_instruction": "Instrucción de movimiento para la IA de video"
    }},
    ... (total 4 escenas)
  ]
}}
"""

AUDIO_PROMPT_STICKMAN = """
Usa un tono barítono, serio, pero muy FLUIDO y ATRACTIVO. No debe sonar robótico. 
Debe sonar como un narrador de cine que cuenta una historia fascinante con pausas dramáticas pero ritmo constante.
Respeta los tiempos para que el total no supere los 29 segundos.

TEXTO A NARRAR:
{audio_text}
"""
