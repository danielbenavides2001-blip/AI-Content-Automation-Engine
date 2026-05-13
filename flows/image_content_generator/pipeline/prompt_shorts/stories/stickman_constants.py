from typing import ClassVar

IDEA_PROMPT_STICKMAN = """
ROL: Eres un experto en SUPERACIÓN PERSONAL, psicología del éxito y guionista de fábulas motivadoras. Tu misión es generar "LECCIONES DE VIDA" de 15-25 segundos que utilicen una metáfora visual para dejar un mensaje de superación personal claro y transformador.

1. NÚCLEO NARRATIVO (Superación Personal)
Cada video debe dejar un mensaje directo que ayude al espectador a mejorar su vida.
Ejes Temáticos: El poder de la disciplina, superar el miedo al fracaso, la importancia del enfoque, construir resiliencia, vencer la procrastinación, la mentalidad de crecimiento, el valor de la constancia.
Símbolos Visuales: Puentes que se desvanecen, jaulas abiertas, sombras que cobran vida, faros en el desierto, llaves de cristal, relojes sin manecillas.

TEMA CENTRAL OBLIGATORIO: {selected_area}
ESTILO VISUAL: Ilustración Digital Atmosférica.

2. ESTRUCTURA DE LA FÁBULA (DURACIÓN 15-25 SEG)
Cada guion debe seguir este arco de revelación:
Escena 1 (El Peso): Presenta una carga o situación limitante (máx 12 palabras).
Escena 2 (La Ilusión): Muestra por qué el personaje no puede escapar o qué cree que es real (máx 12 palabras).
Escena 3 (El Despertar): Un momento de duda o cambio de perspectiva (máx 12 palabras).
Escena 4 (La Revelación): El mensaje final, la "verdad" que libera (máx 8 palabras).
Tono de voz: Sabio, CONTEMPLATIVO, REVELADOR.

REGLA DE SEGURIDAD (IMPORTANTE): Evita descripciones de violencia explícita, sangre o daño físico extremo. Enfócate en la metáfora, la psicología y la representación simbólica del dolor emocional o la lucha interna.

3. DIRECCIÓN DE ARTE (ESTILO PREGUNTAS Y TRIVIAS)
Cada video consta de 4 ilustraciones digitales atmosféricas y vibrantes.
Estilo Visual: "High-quality digital illustration, atmospheric lighting, deep blues and vibrant sunset oranges, cinematic composition, depth of field."
Entornos: Fondos META FÓRICOS y detallados (ej. una isla flotante, un templo circular bajo las estrellas, un camino de luz en el vacío, un árbol brillando en la oscuridad). No es Noir plano; hay color y vida.
Personaje: "An expressive minimalist stickman with a white circular head, clearly visible facial features (expressive eyes/mouth), and a thin black body. The stickman must cast light or be illuminated by the environment (rim lighting)."
Simbología: Incluye elementos que brillan o destacan (un corazón ardiente, una llave dorada, hilos de luz, una llama en la mano).
Paleta de Colores: Colores profundos y saturados. Azules noche, naranjas de atardecer, blancos brillantes y acentos de color vibrante (Amarillo, Dorado o Azul Eléctrico).

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
