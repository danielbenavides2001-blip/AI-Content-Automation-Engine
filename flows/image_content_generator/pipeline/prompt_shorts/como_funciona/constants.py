# Prompt constants for "Cómo funcionan las cosas" (Clean Visual Explainers)

IDEA_PROMPT_COMO_FUNCIONA = """
Eres un estratega audiovisual y divulgador científico de élite para EnigmaIQ en español LATAM.
Tu misión es generar una idea brutalmente fascinante para un video corto (Reel/TikTok) en formato **"¿CÓMO FUNCIONA REALMENTE...?"** o **CURIOSIDAD MECÁNICA/BIOLÓGICA/FÍSICA VISUAL**.

**EL SECRETO DE ESTE FORMATO (ALTA RETENCIÓN Y VIRALIDAD):**
El video debe explicar el mecanismo interno, la física o el secreto anatómico que la gente ve todos los días pero NUNCA ha visto por dentro.
Debe provocar el efecto mental de: *"¡Guau, no tenía idea de que eso funcionaba así!"*.

**CATEGORÍAS DE MÁXIMO IMPACTO:**
1. MECANISMOS E INVENTOS COTIDIANOS: El interior de un candado al girar la llave, cómo un airbag se infla en milisegundos, cómo un reloj automático se da cuerda con tu pulso, el mecanismo interno de un silenciador de pistola, cómo frena un avión al tocar tierra.
2. ANATOMÍA Y CUERPO HUMANO: Cómo un mosquito corta y succiona sangre sin dolor, cómo viaja el veneno de serpiente por las venas, por qué duelen tanto los cortes de papel, cómo se forma una ampolla para protegerte, qué pasa en el cerebro al aguantar un estornudo.
3. NATURALEZA Y FENÓMENOS EXTREMOS: La pinza del camarón pistola que crea calor como el sol, cómo el lagarto cornudo dispara sangre por los ojos, cómo un escarabajo bombardero mezcla químicos a 100°C, por qué el hielo flota en el agua y salva la vida marina.
4. CIENCIA Y FÍSICA SORPRENDENTE: Por qué la Tierra está más cerca del Sol en invierno, cómo se sostiene un puente colgante con cables, cómo viaja la luz por la fibra óptica en el fondo del mar.

**ESTRUCTURA DE LA IDEA:**
- **title**: Título directo, intrigante y en minúsculas limpias con mayúscula inicial (ej: "¿Cómo funciona un candado por dentro?", "Así es como un mosquito te pica sin dolor"). PROHIBIDO agregar corchetes como [Hook B].
- **hook**: La frase inicial de interrupción que romperá el scroll en los primeros 2 segundos (máx 15 palabras).
- **header_title**: Frase técnica corta de 2-4 palabras en MAYÚSCULAS que aparecerá fija arriba (ej: "MECÁNICA INTERNA", "ANATOMÍA SECRETA", "FÍSICA VISUAL", "INGENIERÍA OCULTA").
- **caption**: Descripción cautivadora para Facebook con 4-5 hashtags limpios.

{visual_style}
"""

SCRIPT_PROMPT_COMO_FUNCIONA = """
Eres un director y guionista audiovisual experto en videos explicativos hiper-visuales de 35 a 45 segundos para EnigmaIQ.

Basándote en la IDEA, escribe un guion estructurado en **EXACTAMENTE 5 ESCENAS CORTAS Y PRECISAS**.
Cada escena debe ser un paso lógico en la revelación del mecanismo:

**ESTRUCTURA DE LAS 5 ESCENAS:**
- **Escena 1 (El Gancho - Segundos 0 a 6):** Plantea la anomalía, el misterio o la pregunta visual. Rompe el scroll de inmediato. PROHIBIDO decir "Hola", "¿Sabías qué?", o saludos. Entra directo a la acción.
- **Escena 2 (El Interior Oculto - Segundos 6 a 15):** Corte transversal (cross-section) o vista de rayos X. Muestra las piezas, células o fuerzas que nadie puede ver a simple vista.
- **Escena 3 (La Acción Física - Segundos 15 a 25):** El momento exacto de la reacción: la presión sube, el perno se alinea, el líquido se inyecta o la fuerza se dispara.
- **Escena 4 (La Consecuencia Asombrosa - Segundos 25 a 35):** Por qué este diseño es perfecto o la razón biológica/física por la que ocurre.
- **Escena 5 (El Cierre y Debate - Segundos 35 a 42):** Remata con una conclusión concisa y una pregunta corta y directa para detonar comentarios de la comunidad (ej: "¿Conocías este mecanismo secreto? Te leo en comentarios 👇").

**REGLAS DE ORO DE PRODUCCIÓN:**
1. 🎯 **COHERENCIA AUDIOVISUAL ABSOLUTA (LO QUE SE VE = LO QUE SE NARRA):**
   - Cada escena DEBE mostrar en pantalla el objeto físico exacto, pieza móvil, corte transversal o reacción anatómica que el locutor está pronunciando.
   - PROHIBIDO imágenes metafóricas, abstractas o fondos oscuros genéricos vacíos.
2. 📸 **TIPO VISUAL (`visual_type`):**
   - Usa `"ai_image"` para planos técnicos, cortes transversales (cross-section cutaways), anatomía interna, microfotografía o mecanismos complejos.
   - Usa `"stock_video"` ÚNICAMENTE para planos reales del mundo cotidiano filmable (un avión aterrizando, una mano cerrando una cerradura, olas del mar).
3. 📝 **REGLA DE `image_prompt`:**
   - Comienza SIEMPRE con el sujeto físico exacto y su ángulo: "Detailed cross-section diagram of [mecanismo/órgano], showing internal pins and springs, mechanical blueprint style, cinematic lighting, 8k resolution, vertical 9:16".
4. 📏 **LONGITUD DE NARRACIÓN (RITMO RÁPIDO):**
   - Cada escena debe tener entre **14 y 20 palabras en español (LATAM)**.
   - Duración total de narración: **90 a 115 palabras en total** (garantiza entre 35 y 45 segundos de video, la duración óptima para retención del 85%+).

**FORMATO JSON ESTRICTO POR ESCENA:**
{
  "scene_number": 1,
  "visual_type": "ai_image",
  "image_prompt": "Detailed cross-section cutaway of [sujeto]...",
  "pexels_query": "",
  "narration": "La narración en español aquí...",
  "movement_instruction": "Slow push-in zoom focusing on the core mechanism.",
  "sfx": "mechanical_click"
}
"""

FOCUS_AREAS_COMO_FUNCIONA = [
    "MECANISMOS COTIDIANOS POR DENTRO: El corte transversal de un candado y llave, cómo se infla un airbag, cómo funciona el disparador de un bolígrafo, el mecanismo de un reloj mecánico automático, cómo frena un ascensor si se rompe el cable.",
    "ANATOMÍA Y RESPUESTA DEL CUERPO: La aguja microscópica del mosquito que adormece la piel, cómo los colmillos de serpiente rotan 90 grados como bisagras, por qué una espina de pescado puede pasar o atorarse, cómo la piel crea una ampolla de agua protectora.",
    "ARMAS BIOLÓGICAS DE LA NATURALEZA: La burbuja hirviente del camarón pistola, cómo el escarabajo bombardero mezcla reactivos a 100°C, cómo la medusa dispara dardos microscópicos de veneno en microsegundos.",
    "INGENIERÍA Y FÍSICA OCULTA: Por qué la Tierra está más cerca del Sol en pleno invierno del hemisferio norte, cómo viajan los datos por cables submarinos en el fondo del océano, cómo un puente colgante reparte toneladas de peso con cables tensados.",
    "CURIOSIDADES DE SALUD COTIDIANA: Qué pasa exactamente en los huesos y articulaciones cuando te truenas los dedos, por qué el agua fría congela la parte trasera del paladar en 2 segundos, cómo una gota de pegamento instantáneo cura heridas.",
    "TECNOLOGÍA DE SUPERVIVENCIA Y VEHÍCULOS: Cómo los neumáticos de Fórmula 1 se derriten para pegarse al asfalto, cómo una caja de cambios manual engrana velocidades sin romperse, cómo vuela un dron manteniendo el equilibrio perfecto."
]
