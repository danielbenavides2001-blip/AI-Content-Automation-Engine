IDEA_PROMPT_SIETE_NIVELES = """
Eres un estratega de contenido viral para EnigmaIQ en español LATAM.

Tu tarea es generar una idea poderosa para un video corto (Reel/Short/TikTok) sobre "Los 7 niveles de [TEMÁTICA]".

El formato sigue una progresión clara: 7 niveles donde cada nivel es MÁS IMPACTANTE que el anterior.
El nivel 1 es intrigante. El nivel 7 debe ser ALUCINANTE.

**ESTRUCTURA DE LA IDEA:**
- **title**: Título creativo y descriptivo comenzando con "Los 7 niveles de..."
- **hook**: Gancho de interrupción de 10-15 palabras que genere intriga inmediata
- **intrigue_header**: Frase corta de 3-5 palabras que aparecerá en pantalla (ej: "LUGARES PROHIBIDOS", "ISLAS MISTERIOSAS")
- **caption**: Descripción para redes sociales que invite a ver los 7 niveles

{visual_style}
"""


SCRIPT_PROMPT_SIETE_NIVELES = """
Eres un guionista experto para videos virales de EnigmaIQ en español LATAM.

Vas a escribir un guion para un video de tipo "Los 7 niveles de [TEMÁTICA]".

**REGLAS DE ORO:**
1. El video tiene EXACTAMENTE 8 escenas: 1 INTRO + 7 NIVELES
2. La INTRO (scene_number=1, nivel=0) debe enganchar al espectador con el hook
3. Las 7 escenas siguientes representan un NIVEL cada una (nivel 1 al 7)
4. El NIVEL 1 debe ser interesante pero el más suave
5. El NIVEL 7 debe ser el MÁS IMPACTANTE, alucinante o escalofriante
6. La progresión de impacto debe ser clara y ascendente
7. Entre nivel y nivel, la narración debe generar expectativa del siguiente

**INTRIGUE HEADER:** El campo `intrigue_header` del JSON debe contener una frase corta de 3-5 mayúsculas impactante que aparecerá en pantalla (ej: "LUGARES PROHIBIDOS", "ISLAS MISTERIOSAS"). DEBE coincidir con la temática del video.

**FORMATO POR ESCENA (JSON ESTRICTO - CADA ESCENA DEBE TENER TODOS ESTOS CAMPOS):**

--- ESCENA DE INTRO (nivel=0) ---
```json
{
  "scene_number": 1,
  "nivel": 0,
  "titulo_nivel": "",
  "impacto": "Bajo",
  "visual_type": "stock_video",
  "image_prompt": "Mysterious establishing shot...",
  "pexels_query": "keywords",
  "narration": "El hook del video aquí... una frase que enganche.",
  "sfx": "mysterious"
}
```

--- ESCENAS DE NIVEL (nivel=1 al 7) ---
```json
{
  "scene_number": 2,
  "nivel": 1,
  "titulo_nivel": "Título corto del nivel",
  "impacto": "Bajo",
  "visual_type": "stock_video",
  "image_prompt": "Detailed image prompt in English...",
  "pexels_query": "keywords",
  "narration": "Nivel 1: [dato intrigante...]",
  "sfx": "mysterious"
}
```

**REGLAS ESTRICTAS DE NARRACIÓN (NO NEGOCIABLE - CADA NARRACIÓN DEBE EMPEZAR EXACTAMENTE ASÍ):**

- INTRO (nivel=0): La narración DEBE ser el hook del video. Una frase corta que enganche. SIN empezar con "Nivel". Ej: "Hay lugares en el mundo a los que está prohibido entrar." o "Existen sitios que los gobiernos no quieren que veas."
- Nivel 1: La narración DEBE empezar TEXTUALMENTE con "Nivel 1: " o "Empezamos en el nivel 1: ". NADA de preguntas retóricas ni hooks. El espectador debe ESCUCHAR "Nivel 1" en los primeros 2 segundos. La narración del nivel 1 DEBE describir el lugar REAL del titulo_nivel (ej. si el título es "La base más secreta", la narración debe describir esa base, no hacer una pregunta genérica).
- Nivel 2: "Subimos al nivel 2: "
- Nivel 3: "Llegamos al nivel 3: "
- Nivel 4: "El nivel 4 es aún más impactante: "
- Nivel 5: "El nivel 5 es donde las cosas se ponen realmente [adjetivo]: "
- Nivel 6: "El nivel 6 nos lleva al límite: "
- Nivel 7: "Y llegamos al nivel final, el nivel 7: "

**EJEMPLO CORRECTO DE INTRO:**
✅ BIEN: "Hay lugares en la Tierra cuyo acceso está terminantemente prohibido. Hoy vamos a conocer los 7 más impactantes."
✅ BIEN: "Olvídate de los mapas turísticos. Estos son los 7 lugares más prohibidos del planeta."

**EJEMPLO CORRECTO DE NARRACIÓN PARA NIVEL 1:**
❌ MAL: "Nivel 1: ¿Qué horrores o maravillas guardan los rincones más inaccesibles del mundo?" (es pregunta retórica, no describe el nivel)
✅ BIEN: "Empezamos en el nivel 1: hay una base militar en el desierto de Nevada cuyo nombre oficial ni siquiera existe."

**EJEMPLO CORRECTO DE NARRACIÓN PARA NIVEL 7:**
✅ BIEN: "Y llegamos al nivel final, el nivel 7: el secreto más guardado de la humanidad. Si te gustó, comparte este video con alguien que ame los misterios."

**IMPORTANTE:** La escena 1 debe tener nivel=0 (INTRO). Las escenas 2-8 deben tener nivel=1 al 7. Cada escena DEBE tener scene_number secuencial del 1 al 8. En la intro, titulo_nivel debe ser "" (vacío). No uses preguntas retóricas en ninguna narración.

**IMPORTANTE:** Cada nivel debe ser un caso, lugar o fenómeno REAL y verificable. Nada de ficción.
"""


FOCUS_AREAS_SIETE_NIVELES = [
    "DEPREDADORES PREHISTÓRICOS Y MONSTRUOS EXTINTOS: Criaturas colosales del pasado más aterradoras que el T-Rex, monstruos marinos de hace millones de años (Megalodón, Mosasaurio, Basilosaurio, Titanoboa, aves del terror).",
    "REINO ANIMAL INSÓLITO Y ADAPTACIONES EXTREMAS: Animales con habilidades alienígenas en la Tierra, criaturas con venenos paralizantes, bioluminiscencia abisal, defensas de pesadilla, camuflaje óptico y sentidos imposibles.",
    "ABISMOS MARINOS Y CRIATURAS DE LA ZONA HADAL: Especies de las profundidades de la Fosa de las Marianas, fosas inexploradas, anomalías acústicas submarinas, fuentes hidrotermales y ecosistemas donde nunca llega la luz.",
    "PARADOJAS DEL UNIVERSO Y FÍSICA ROTA: Agujeros negros supermasivos, exoplanetas con climas de pesadilla (lluvia de vidrio, vientos de hierro líquido), estrellas zombi, el vacío cósmico de Boötes y anomalías del espacio-tiempo.",
    "FENÓMENOS GEOLÓGICOS QUE DESAFÍAN LA CIENCIA: Lugares en la Tierra que parecen de otro planeta (el Ojo del Sahara, volcanes de lava azul de Kawah Ijen, lagos explosivos, cuevas de cristales gigantes de Naica).",
    "CIVILIZACIONES PERDIDAS Y ARQUEOLOGÍA INEXPLICABLE: Ciudades sumergidas hace 10,000 años, templos megalíticos tallados en roca madre sólida, tumbas intactas y misterios de la historia antigua.",
    "ARTEFACTOS FUERA DEL TIEMPO (OOPARTS): Reliquias milenarias con tecnología anacrónica, mapas antiguos imposibles, engranajes milenarios y baterías ancestrales.",
    "INGENIOS Y MECANISMOS ANCESTRALES: Inventos olvidados de la antigüedad (el Mecanismo de Anticitera, arquitectura antisísmica milenaria de Japón y los Incas, fuego griego, acueductos imposibles).",
    "HAZAÑAS DE SUPERVIVENCIA HUMANA EXTREMA: Personas que sobrevivieron a caídas desde aviones sin paracaídas, naufragios de meses en el océano abierto, congelamiento médico y retorno a la vida.",
    "ANOMALÍAS MÉDICAS Y DEL CUERPO HUMANO: Mutaciones genéticas extraordinarias reales (personas que no sienten dolor, visión tetracromática, memoria autobiográfica total), casos médicos que desafían la biología.",
    "LUGARES PROHIBIDOS Y BÓVEDAS SECRETAS: Sitios de acceso vetado en la Tierra, búnkers impenetrables, bóvedas globales (Svalbard) y archivos celosamente guardados.",
    "CIUDADES SUBTERRÁNEAS Y TÚNELES SECRETOS: Ciudades bajo tierra como Derinkuyu en Capadocia, redes de túneles secretos milenarios y complejos militares bajo roca sólida.",
    "ISLAS MISTERIOSAS Y AISLADAS: Islas volcánicas inaccesibles, atolones prohibidos, islas infestadas de especies únicas y territorios remotos que rompen la geografía.",
    "EXPERIMENTOS CIENTÍFICOS PERTURBADORES: Experimentos históricos revolucionarios de la psicología y la física que pusieron a prueba los límites del conocimiento y la mente humana.",
    "RÉCORDS EXTREMOS Y LÍMITES DE LA MATERIA: Las temperaturas más extremas jamás creadas en laboratorio, el material más oscuro y resistente del cosmos, el sonido más ensordecedor registrado en la Tierra.",
    "MISTERIOS SIN RESOLVER DE LA HISTORIA: Expediciones que se desvanecieron sin dejar rastro, códigos y manuscritos indescifrables como el Manuscrito Voynich.",
    "FRONTERAS EXTRAÑAS Y RAREZAS DEL MAPA: Enclaves absurdos, fronteras que atraviesan casas, líneas geopolíticas que desafían la lógica del planeta.",
    "CIUDADES ABANDONADAS Y LUGARES EN PAUSA: Metrópolis desiertas donde la naturaleza tomó el control, complejos industriales fantasma, pueblos congelados en el tiempo.",
    "LUGARES PELIGROSOS Y CONDICIONES MORTALES: Sitios donde la atmósfera te quitaría la vida en minutos, lagos de ácido, desiertos donde jamás ha llovido.",
    "REINO FÚNGICO Y VEGETAL INSÓLITO: Hongos bioluminiscentes, organismos que controlan la mente de insectos (Cordyceps), plantas carnívoras gigantes y seres vivos milenarios."
]


AUDIO_PROMPT_SIETE_NIVELES = """
Narrator tone: Deep, mysterious, and progressively more intense. Start calm and intriguing for level 1, and build tension with each level until level 7 which should sound dramatic and mind-blowing.

TEXT TO NARRATE:
{audio_text}
"""
