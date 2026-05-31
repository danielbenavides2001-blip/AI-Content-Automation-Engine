# Constantes de Prompts para Fútbol y Mundial - EnigmaIQ Football

IDEA_PROMPT_FOOTBALL = """
Eres el Productor Principal de "EnigmaIQ Football", cubriendo las curiosidades y enigmas más sorprendentes, misteriosos e históricamente exactos del fútbol y la historia de los Mundiales.
Genera un concepto e idea cinematográfica de alta retención basado estrictamente en hechos reales verificados históricamente.

**LÓGICA DEL TITULAR SUPERIOR (La barra del gancho):**
Debes generar un hecho impactante para el campo `top_headline` (Titular Superior). Debe estar redactado como una "Verdad Incomoda" o un "Secreto" que dispare el ego o la curiosidad del espectador.
- Mal: "Mussolini influyó en el Mundial."
- Bien: "MUSSOLINI DECRETÓ: VENCER O MORIR."
- Mal: "Un perro encontró la Copa del Mundo robada."
- Bien: "UN PERRO SALVÓ EL MUNDIAL DE 1966."
- Mal: "Francia vistió camisetas distintas."
- Bien: "FRANCIA JUGÓ CON CAMISETAS DE PESCA."

El titular DEBE estar siempre en MAYÚSCULAS, ser estático y llamativo.

**REGLA OBLIGATORIA DE EXACTITUD HISTÓRICA:**
Cada dato debe ser 100% real históricamente. No inventes partidos, goles, nombres, fechas, resultados ni estadísticas. Si un dato no está verificado al 100%, exclúyelo.

**CAMPOS OBLIGATORIOS DE SALIDA (EN ESPAÑOL):**
- `title`: Un título optimizado para el video.
- `top_headline`: El texto de la barra superior en MAYÚSCULAS.
- `hook`: La frase de disrupción inicial (10-15 palabras) que enganche.
- `caption`: Una descripción profunda y muy detallada para redes sociales que explique el misterio/historia a fondo, acompañada de 10 hashtags virales (debe incluir #EnigmaIQ #Fútbol #Mundial).
"""

AUDIO_PROMPT_FOOTBALL = """
Usa un tono narrativo que sea educativo pero altamente intrigante, dramático y dinámico. Como un experto revelando un misterio o secreto histórico del fútbol.

TEXTO A NARRAR:
{audio_text}
"""

SCRIPT_PROMPT_FOOTBALL = """
Eres el Productor Principal de "EnigmaIQ Football."
Basado en la IDEA proporcionada, escribe un guion de video para un Reel que dure entre 50 y 60 segundos.
Divide la historia en exactamente **6 a 8 escenas cortas** para mantener los niveles de dopamina del espectador con cambios rápidos de plano.

**1. ESTRUCTURA DEL GUION (100% HECHOS HISTÓRICOS REALES):**
- **Escena 1 [0-5s] (La Disrupción):** Debe empezar obligatoriamente con: "La mayoría piensa que [X], pero la realidad es [aterradora/increíble/incomprensible]."
- **Escenas 2-6 [5-45s] (La Evidencia):** Proporciona exactamente 3 datos históricos rápidos y contundentes que demuestren el titular. Usa un lenguaje muy sensorial y activo (ej. "tacos de cuero embarrados", "luces volumétricas de estadio", "entrada de papel vieja y rasgada").
- **Última Escena [45-60s] (El Bucle de Paradoja):** Termina con una pregunta intrigante que obligue a los usuarios a volver a ver el video para cerrar el bucle.

**2. ESTILO VISUAL: "Vintage Collage & Scrapbook" (Prompts para Vertex AI):**
Para el campo `image_prompt` de cada escena, escribe una descripción física muy detallada de la escena en inglés (ya que la IA entiende mejor inglés) usando la estética de "Vintage Collage & Scrapbook".
Debes construir el prompt utilizando exactamente esta plantilla, rellenando las variables en corchetes en inglés:
"A mixed-media scrapbook collage representing [Scene visual concept]. A faded sepia-toned retro Polaroid photo showing [Specific action/event of the scene], a torn piece of yellowed fibrous newspaper with a dynamic bold headline saying '[SHORT 2-3 WORD CUSTOM HEADLINE]', a [Focal football object like a vintage laced soccer ball, muddy leather cleats, brass referee whistle, or old goalkeeper glove] in sharp focus in the foreground, handwritten tactical play arrows and chalk lines on a warm craft paper background. Volumetric nostalgic lighting, soft shadows, extremely realistic paper textures, photorealistic macro shot, 8k."

*Nota: Varía el objeto focal de fútbol (botas, silbato, balón, guantes, ticket) y el TITULAR DEL PERIÓDICO en cada escena para evitar que las imágenes sean repetitivas. No incluyas rostros reales y reconocibles de jugadores conocidos para evitar derechos de imagen; enfócate en siluetas retro, objetos y ambientaciones.*

**3. ESQUEMA DE ESCENA:**
Para cada escena, define:
1. `scene_number`: Entero secuencial.
2. `visual_type`: Debe ser `"ai_image"`.
3. `image_prompt`: La descripción en inglés que coincida con el estilo Vintage Scrapbook.
4. `narration`: La narración hablada exacta EN ESPAÑOL. Mantén todo el guion por debajo de 120 palabras para que quepa en 60 segundos.
5. `pexels_query`: Dejar vacío.

**LA NARRACIÓN, TÍTULO Y CAPTION DEBEN ESTAR EN ESPAÑOL. SOLO LOS IMAGE_PROMPTS DEBEN ESTAR EN INGLÉS.**
"""

FOCUS_AREAS_FOOTBALL = [
    "EL ROBO DE LA COPA DE 1966: Cómo el trofeo Jules Rimet fue robado de una iglesia en Londres y encontrado en un arbusto por un perro llamado Pickles.",
    "EL GENIO DESCALZO DE 1938: Cómo la estrella brasileña Leônidas da Silva anotó un legendario gol descalzo bajo el barro en pleno mundial porque su bota se rompió.",
    "LAS CAMISETAS DE UN CLUB DE PESCA EN 1978: Por qué la selección de Francia tuvo que jugar un partido del Mundial contra Hungría vistiendo las camisetas a rayas verde y blanca del club local Kimberley.",
    "EL MANCO CAMPEÓN DE 1930: Cómo Héctor Castro, a quien le faltaba el antebrazo derecho, anotó el gol decisivo en la primera final de la historia para coronar a Uruguay.",
    "EL MISTERIO DE MWEPU EN 1974: El jugador de Zaire que pateó la pelota antes del tiro libre de Brasil por pánico absoluto a las amenazas de muerte de su dictador si perdían por goleada.",
    "LA GUERRA DEL BALÓN EN 1930: Cómo Argentina y Uruguay jugaron la final del Mundial con dos balones distintos (uno de cada país) al no ponerse de acuerdo sobre cuál usar.",
    "EL ULTIMATUM DE MUSSOLINI EN 1934: El telegrama que el dictador italiano mandó a los jugadores con dos palabras: 'Vencer o Morir' antes del partido final.",
    "LOS TACOS MILAGROSOS DE 1954: Cómo Alemania venció a la invencible selección de Hungría bajo la tormenta gracias a los revolucionarios tacos intercambiables inventados por Adi Dassler.",
    "EL PSICÓLOGO QUE RECHAZÓ A PELÉ EN 1958: El día que el psicólogo de Brasil declaró oficialmente a Pelé (de 17 años) 'infantil e incapacitado mentalmente' para jugar el Mundial.",
    "LA BATALLA DE SANTIAGO EN 1962: Uno de los partidos más violentos de los Mundiales entre Chile e Italia, donde la policía militar tuvo que intervenir tres veces para separar a los jugadores.",
    "EL TRÁGICO AUTOGOL DE 1994: La triste historia de Andrés Escobar y las consecuencias del autogol contra Estados Unidos en el Mundial de 1994.",
    "EL GOL FANTASMA DE 1966: El misterio eterno sobre si el tiro de Geoff Hurst cruzó realmente la línea en la final de Inglaterra 1966 contra Alemania.",
    "LA MISTERIOSA SUPLENCIA DE 1938: Por qué el seleccionador de Brasil dejó en la banca a su estrella Leônidas para la semifinal contra Italia diciendo que 'lo guardaba para la final' (la cual perdieron).",
    "EL PARTIDO DE LA NIEBLA DE 1945: El mítico Arsenal vs Dynamo de Moscú jugado en una niebla tan densa que jugaron con hasta 15 jugadores en el campo y un expulsado regresó a escondidas.",
    "LAS CAMISETAS DEL MERCADO EN 1986: Cómo Carlos Bilardo compró camisetas de algodón azul en un mercado de Ciudad de México 48 horas antes de jugar contra Inglaterra, pegándole los escudos con planchas.",
    "LA MALDICIÓN DE BÉLA GUTTMANN EN EL BENFICA: La profecía del técnico que impide al club ganar una final europea durante 100 años (ya llevan 8 finales europeas perdidas consecutivamente).",
    "LA PROTOTESTA DEL 149-0 EN 2002: El insólito partido de la liga de Madagascar donde los jugadores del SO l'Emyrne se metieron 149 autogoles para protestar un mal arbitraje."
]
