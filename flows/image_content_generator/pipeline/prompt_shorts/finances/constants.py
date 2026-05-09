# flake8: noqa: E501
AUDIO_PROMPT: str = "{audio_text}"

# --- NUEVA SERIE: ENIGMAIQ - CÓDIGOS DE RIQUEZA ---
IDEA_PROMPT_MINDSET: str = """# 🧠 GENERADOR DE IDEAS — SERIE: ENIGMAIQ (CÓDIGOS DE RIQUEZA)
**Objetivo:** Generar una lección de finanzas brutales, hábitos de riqueza o críticas a la mentalidad de pobreza.

**DIRECTIVA DE VARIEDAD INFINITA:**
Explora territorios psicológicos y prácticos sin repetir conceptos:
- **Hábitos Invisibles:** Gastos hormiga, inflación del estilo de vida, gratificación instantánea.
- **Disciplina de Hierro:** Madrugar, lectura, ahorro forzado, el "no" como superpoder.
- **Realidad Brutal:** Por qué los pobres siguen pobres, la trampa de la clase media, la mentira de los títulos.
- **Psicología del Dinero:** Miedo a invertir, envidia al éxito, mentalidad de escasez vs abundancia.
- **Sistemas de Riqueza:** Interés compuesto, activos vs pasivos, libertad vs seguridad.

**Reglas:**
- Título: Debe ser provocador y directo (sin números de parte).
- Tono: Crudo, directo, realista y premium.
- No repitas el mismo ángulo bajo ninguna circunstancia.
"""

# --- NUEVO MOTOR DE IMÁGENES SKETCH (ESTILO CÓDIGO MILLONARIO) ---
IMAGE_INTERACTION_PROMPT: str = """# 🧩 GENERADOR DE ACERTIJOS VISUALES — ESTILO SKETCH MINIMALISTA
**OBJETIVO:** Generar una imagen tipo boceto a mano que represente un dilema financiero.

**ESTILO VISUAL OBLIGATORIO (ENIGMAIQ):** 
Hand-drawn sketch style, thick clean lines, minimalist white stickman character, expressive facial features (sweat, wide eyes, exhaustion, or calm smile). 
Background: Warm cream or light beige paper texture. 
Colors: Mostly black and white, with strategic highlights in Emerald Green (money), Bright Yellow (gold), or Electric Blue (tech/screens).

**FORMATO DE RESPUESTA OBLIGATORIO (JSON):**
{
  "idea_visual": "Boceto del personaje frente a un dilema (ej: dos puertas, un grifo que gotea monedas)",
  "image_prompt": "Minimalist hand-drawn sketch, clean thick lines, warm cream background, [DESCRIPCIÓN DE LA ESCENA CON EL STICKMAN EXPRESIVO], emerald green highlights for money elements, high contrast, 4k.",
  "caption": "Caption corto, crudo y que genere una pregunta al espectador.",
  "objetivo_psicologico": "Reflexión o Culpa"
}
"""

# Alias de compatibilidad
IDEA_PROMPT_ESTRATEGIA: str = IDEA_PROMPT_MINDSET
IDEA_PROMPT_HUSTLE: str = IDEA_PROMPT_MINDSET
IDEA_PROMPT_CHEATSHEET: str = IDEA_PROMPT_MINDSET

SCRIPT_PROMPT: str = """# 📝 GUIONISTA DE REALIDAD BRUTAL — SERIE: ENIGMAIQ
**Objetivo:** Crear un guion de 4 escenas que pegue fuerte en la mente del espectador sobre sus finanzas.

**ESTILO VISUAL (STORYBOARD):**
- Escenas tipo boceto (Sketch) con fondo crema y stickman blanco expresivo.
- Usa colores solo para el dinero (Verde) o el peligro (Rojo/Azul).

**Estructura Narrativa (4 Escenas):**
1. **Escena 1 (Hook):** Una frase que ataque directamente un ego o un mal hábito.
2. **Escena 2 (El Error):** Mostrar visualmente el error (ej: comprar un café caro mientras el bolsillo está roto).
3. **Escena 3 (La Realidad):** Explicar por qué eso te mantiene estancado. Usa datos o lógica fría.
4. **Escena 4 (Cierre Maestro):** Una invitación a despertar y unirse a la élite + "Síguenos en EnigmaIQ".

**Reglas del Voice Over:**
- Tono: Barítono, pausado, autoritario pero pedagógico.
- Duración: Exactamente 25-30 palabras por escena para un video de 55-60 segundos.
- Lenguaje: Usa "Tú". No uses tecnicismos innecesarios, sé directo.

**image_prompt (INGLÉS):**
- Estilo: Minimalist hand-drawn sketch, clean thick lines, warm cream background, white stickman.
- Escena 1: Stickman in a powerful or reflective pose.
- Escena 2: Stickman interacting with the "problem" (e.g., credit card, luxury items).
- Escena 3: Stickman facing the "consequence" or "logic" (e.g., an empty safe, a wall of books).
- Escena 4: Close up of the stickman smiling or pointing forward, emerald green details.
"""
