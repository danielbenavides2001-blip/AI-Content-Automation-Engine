# flake8: noqa: E501
AUDIO_PROMPT: str = "{audio_text}"

# --- NUEVA SERIE: FORMAS COCHINAS DE GANAR DINERO ---
IDEA_PROMPT_MINDSET: str = """# 🧠 GENERADOR DE IDEAS — SERIE: FORMAS COCHINAS DE GANAR DINERO
**Objetivo:** Generar una estrategia financiera real pero éticamente gris, basada en vacíos legales o psicología oscura.

**DIRECTIVA DE VARIEDAD INFINITA:**
En cada iteración, selecciona un nicho COMPLETAMENTE DIFERENTE al anterior. Explora estos territorios:
- **Bienes Raíces:** Embargos preventivos, usufructos vitalicios, flipping de nuda propiedad.
- **Corporativo:** Compra de empresas en quiebra por sus activos, ingeniería fiscal, paraísos legales.
- **Tecnología:** Arbitraje de clics, dominios de marcas olvidadas, copyright de IA, algoritmos de apuestas.
- **Finanzas Puras:** Arbitraje de tasas, swaps de deuda, manipulación de micro-volatilidad.
- **Seguros y Leyes:** Cobro de pólizas inactivas, vacíos en seguros de vida, litigación masiva.

**Reglas:**
- Título: Debe seguir el formato "[Formas cochinas de ganar dinero - Parte X] Título Provocador".
- Tono: Maquiavélico, cínico y profesional.
- No repitas el mismo ángulo bajo ninguna circunstancia.
"""

# --- NUEVO MOTOR DE IMÁGENES NOIR (SERIE COCHINA) ---
IMAGE_INTERACTION_PROMPT: str = """# 🧩 GENERADOR DE ACERTIJOS VISUALES — ESTILO NOIR / PODER
**OBJETIVO:** Generar una imagen tipo acertijo o dilema con el personaje de la serie.

**PERSONAJE OBLIGATORIO:** 
Premium stickman character, round white head, no nose/mouth, wearing classic black sunglasses, black fedora with blue ribbon, formal black suit, white shirt, blue tie, black leather gloves.

**FORMATO DE RESPUESTA OBLIGATORIO (JSON):**
{
  "idea_visual": "Escena del personaje en oficina de lujo, calle oscura o juzgado",
  "image_prompt": "Detailed comic illustration, clean lines, saturated colors, dark noir atmosphere, [DESCRICIÓN DEL PERSONAJE], [ESCENA]",
  "caption": "Caption cínico y directo para Facebook",
  "objetivo_psicologico": "Curiosidad o Poder"
}

**ESTILO:** Cómic detallado, atmósfera oscura, colores saturados.
"""

# Alias de compatibilidad
IDEA_PROMPT_ESTRATEGIA: str = IDEA_PROMPT_MINDSET
IDEA_PROMPT_HUSTLE: str = IDEA_PROMPT_MINDSET
IDEA_PROMPT_CHEATSHEET: str = IDEA_PROMPT_MINDSET

SCRIPT_PROMPT: str = """# 📝 GUIONISTA MAQUIAVÉLICO — SERIE: FORMAS COCHINAS DE GANAR DINERO
**Objetivo:** Crear un guion de 4 escenas que explique una estrategia gris.

**PERSONAJE EN TODAS LAS ESCENAS:** 
White-headed cartoon character in black suit, fedora, and sunglasses.

**Estructura Narrativa (4 Escenas):**
1. **Escena 1 (Hook):** "Formas cochinas de ganar dinero, Parte [X]". Exponer el problema o la oportunidad cínicamente.
2. **Escena 2 (Paso 1 y 2):** Explicar el inicio de la estrategia usando términos reales (arbitraje, vacío legal).
3. **Escena 3 (Paso 3 y Clímax):** La ejecución final y el beneficio monetario.
4. **Escena 4 (Cierre de Poder):** Frase que humille el trabajo tradicional + "Síguenos en EnigmaIQ".

**Reglas del Voice Over:**
- Tono: Cínico, profesional, directo. Sin disculpas.
- Escribe 25-30 palabras por escena (total 50-60 segundos).
- Usar siempre "Tú".

**image_prompt (INGLÉS):**
- Escena 1: Personaje sentado en oficina de lujo con sombras marcadas.
- Escena 2: Personaje manipulando documentos o pantallas digitales.
- Escena 3: Personaje con maletín o símbolos de riqueza en entorno oscuro.
- Escena 4: Close up del personaje sonriendo (solo se ve la boca) con fondo de ciudad nocturna.
- Estilo: Detailed comic illustration, clean lines, noir atmosphere.
"""
