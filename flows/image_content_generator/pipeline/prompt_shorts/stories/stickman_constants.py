from typing import ClassVar

IDEA_PROMPT_STICKMAN = """
ROL: Eres un experto en psicología conductual, guionista de cine negro y artista conceptual. Tu misión es generar contenido para videos de SUPERACIÓN PERSONAL e impacto psicológico de ENTRE 15-25 segundos divididos en 4 escenas visuales potentes.

1. MOTOR DE ORIGINALIDAD (Cero Repetición)
Para cada nuevo video, debes elegir un Eje Temático y un Símbolo Visual.
Ejes Temáticos disponibles: Resiliencia, Disciplina, Superación de miedos, Propósito, Enfoque, Crecimiento interno, Gratitud, Poder mental, Stoicism.
Símbolos Visuales Prohibidos de repetir (SI YA SE USARON): Hilos de títere, Mesas que se encogen, Sombrillas/Lluvia, Puertas de búnker, Espejos, Relojes de arena.

TEMA CENTRAL OBLIGATORIO: {selected_area}
ESTILO VISUAL: Estilo Noir, Minimalist 2D hand-drawn.

2. REGLAS DEL GUION (DURACIÓN 15-25 SEG)
El guion debe durar entre 15-25 segundos totales. El texto debe ser lapidario, rítmico y potente.
Escena 1 (El Desafío): Frase de impacto sobre la lucha (máx 12 palabras).
Escena 2 (La Resistencia): Por qué es difícil avanzar (máx 12 palabras).
Escena 3 (La Transformación): El cambio de perspectiva (máx 12 palabras).
Escena 4 (La Victoria): Frase final de poder y cierre (máx 8 palabras).
Tono de voz: Serio, MOTIVADOR, AUTORITARIO.

REGLA DE SEGURIDAD (IMPORTANTE): Evita descripciones de violencia explícita, sangre o daño físico extremo. Enfócate en la metáfora, la psicología y la representación simbólica del dolor emocional o la lucha interna.

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
  "hook": "Gancho de interrupción (MÁX 10 palabras)",
  "selected_theme": "El eje temático elegido",
  "selected_symbol": "El símbolo visual elegido",
  "scenes": [
    {{
      "scene_number": 1,
      "narration": "Texto ultra-corto de 4 segundos",
      "image_prompt": "Prompt en inglés siguiendo el estilo Noir",
      "movement_instruction": "Instrucción de movimiento para la IA de video"
    }},
    ... (total 4 escenas)
  ]
}}
"""

AUDIO_PROMPT_STICKMAN = """
Usa un tono barítono, serio, pero muy FLUIDO y ATRACTIVO. 
El texto es muy corto, por lo que debes darle peso a cada palabra con pausas estratégicas.
El video total debe durar entre 15 y 25 segundos. No más.

TEXTO A NARRAR:
{audio_text}
"""
