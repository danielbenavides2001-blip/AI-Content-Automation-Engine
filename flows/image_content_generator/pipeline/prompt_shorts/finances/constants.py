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

# --- NUEVO MOTOR DE IMÁGENES SKETCH (ESTILO INFOGRAFÍA ENIGMAIQ) ---
IMAGE_INTERACTION_PROMPT: str = """# 🧩 GENERADOR DE INFOGRAFÍAS — ESTILO SKETCH (PEN & INK)
**OBJETIVO:** Generar un dibujo a tinta que compare dos situaciones financieras con etiquetas en ESPAÑOL.

**ESTILO VISUAL OBLIGATORIO (ENIGMAIQ):** 
- **Estilo**: Detailed hand-drawn pen and ink sketch on warm cream paper. 
- **Técnica**: Thick clean black lines, cross-hatching shadows, minimalist style, high contrast.
- **Contenido**: A split-screen comparison: on the left, [SITUACIÓN 1]; on the right, [SITUACIÓN 2].
- **Texto en Imagen**: Usa etiquetas simples en ESPAÑOL (ej: "Pobre" vs "Rico", "Error" vs "Acierto", "Mentalidad de Escasez" vs "Abundancia").
- **Personaje**: Expressive cartoon stickman, New Yorker cartoon aesthetic.
- **NO USAR**: Realistic photos, 3D, gradients, cinematic lighting.

**FORMATO DE RESPUESTA OBLIGATORIO (JSON):**
{
  "title": "Título corto y potente",
  "hook": "Gancho para detener el scroll",
  "idea_visual": "Comparación: Hábito pobre vs Hábito rico",
  "image_prompt": "Detailed hand-drawn pen and ink sketch on warm cream paper. A split-screen comparison with SPANISH LABELS. Left: [SITUACIÓN 1 con etiqueta 'Pobre']. Right: [SITUACIÓN 2 con etiqueta 'Rico']. Thick clean black lines, cross-hatching shadows, minimalist style, high contrast, clean white and black, emerald green highlights for money elements. No realistic photos, no 3D. New Yorker cartoon aesthetic.",
  "caption": "Pregunta cruda para Facebook.",
  "objetivo_psicologico": "Contraste"
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
