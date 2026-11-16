import json
from pathlib import Path

# 30 Complete Videos x 5 Curiosities = 150 Unique, High-Retention, Non-Repeating Curiosities
# Calibrated for > 60s duration (target: 67-75s) with XpressTV CUDA Voice & MediaHub Stock Matching

CATALOG = [
    # Video 21: Cuerpo & Misterios Vol 1
    {
        "id": "21_EnigmaIQ_5_Cosas_Vol1",
        "title": "5 Cosas que NO sabías hace un minuto 🤯⏳",
        "headline_top": "5 COSAS ASOMBROSAS QUE",
        "headline_bottom": "NO SABÍAS HACE UN MINUTO",
        "category": "CURIOSIDADES DEL MUNDO",
        "description": "5 Cosas y datos curiosos que te volarán la cabeza en menos de un minuto 🤯 Desde el color real de los espejos hasta el secreto del parche pirata.\n\n#EnigmaIQ #XpressTV #Curiosidades #DatosCuriosos #Aprender #Ciencia #SabiasQue #Misterios",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. Aunque creas que un espejo es plateado, en realidad es de un sutil color verde.",
                "p2": "Al rebotar en un túnel de espejos infinitos, la luz se absorbe y el fondo siempre se torna verde oscuro.",
                "q1": "woman looking in mirror reflection",
                "q2": "infinity mirror tunnel green lights"
            },
            {
                "num": 2,
                "p1": "Número dos. Los piratas no usaban parche por ser tuertos, sino para tener un ojo adaptado a la oscuridad.",
                "p2": "Al abordar y saltar a las bodegas enemigas, se cambiaban el parche de ojo y veían perfectamente al instante.",
                "q1": "old pirate ship sailing ocean waves",
                "q2": "human eye pupil dilating dark close up"
            },
            {
                "num": 3,
                "p1": "Número tres. Aunque estés en el Polo Norte a cuarenta grados bajo cero, tus ojos jamás se congelarán.",
                "p2": "Las sales y grasas de tus lágrimas, junto al calor constante de tu sangre, evitan que se forme hielo en ellos.",
                "q1": "snowstorm blizzard freezing winter face",
                "q2": "eye blinking close up macro tears"
            },
            {
                "num": 4,
                "p1": "Número cuatro. El olor a tierra mojada tras la lluvia se llama científicamente petricor.",
                "p2": "Tu nariz es tan sensible a esta bacteria del suelo que puedes detectarla mejor que un tiburón oliendo sangre en el mar.",
                "q1": "rain drops falling dry soil slow motion",
                "q2": "shark swimming deep blue ocean water"
            },
            {
                "num": 5,
                "p1": "Número cinco. Un bebé recién nacido llega al mundo con aproximadamente trescientos huesos blandos.",
                "p2": "Pero al llegar a la adultez solo tienes doscientos seis huesos, ya que la gran mayoría se fusionan conforme vas creciendo.",
                "q1": "cute baby crawling playing happy",
                "q2": "medical x-ray skeleton human bones 3d"
            }
        ]
    },

    # Video 22: Reino Animal Insólito Vol 1
    {
        "id": "22_EnigmaIQ_5_Cosas_Vol2",
        "title": "5 Secretos ANIMALES que parecen de ciencia ficción 🐙🦈",
        "headline_top": "5 SECRETOS ANIMALES QUE",
        "headline_bottom": "PARECEN CIENCIA FICCIÓN",
        "category": "REINO ANIMAL & OCÉANOS",
        "description": "El reino animal esconde secretos imposibles 🐙 Los pulpos tienen 3 corazones y los tiburones son más viejos que los árboles.\n\n#EnigmaIQ #Animales #Naturaleza #Curiosidades #Biologia #XpressTV #DatosCuriosos",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. Los pulpos tienen tres corazones y su sangre es de un intenso color azul.",
                "p2": "Esto se debe a que usan hemocianina rica en cobre en lugar de hierro para transportar oxígeno en aguas congeladas.",
                "q1": "octopus swimming underwater coral reef",
                "q2": "blue liquid test tube laboratory chemistry"
            },
            {
                "num": 2,
                "p1": "Número dos. Los tiburones son mucho más antiguos en el planeta que los propios árboles terrestres.",
                "p2": "Llevan más de cuatrocientos millones de años nadando en los océanos, sobreviviendo a cuatro extinciones masivas globales.",
                "q1": "great white shark swimming clear ocean",
                "q2": "ancient redwood forest giant trees fog"
            },
            {
                "num": 3,
                "p1": "Número tres. Los gatos son los únicos mamíferos carnívoros que no pueden saborear nada dulce.",
                "p2": "Carecen del gen funcional receptor del azúcar en su lengua, por lo que pasteles o golosinas les resultan totalmente insípidos.",
                "q1": "cat face close up licking whiskers",
                "q2": "sweet delicious chocolate cake table"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Las hormigas obreras jamás duermen un sueño continuo como los humanos.",
                "p2": "En su lugar toman pequeñas micro siestas de un minuto unas doscientas cincuenta veces al día para mantenerse activas.",
                "q1": "ants walking carrying leaf macro closeup",
                "q2": "sleeping person comfortable bedroom bed"
            },
            {
                "num": 5,
                "p1": "Número cinco. Los flamencos pueden beber agua casi hirviendo de lagos y géiseres volcánicos sin quemarse.",
                "p2": "La dura piel escamosa de sus patas y su pico especializado filtran agua alcalina tóxica que mataría a cualquier otro animal.",
                "q1": "pink flamingos standing volcanic lake",
                "q2": "boiling water hot geyser steam landscape"
            }
        ]
    },

    # Video 23: Objetos Cotidianos Secretos Vol 1
    {
        "id": "23_EnigmaIQ_5_Cosas_Vol3",
        "title": "5 Objetos que usas TODOS los DÍAS y no sabes su secreto 👖🔒",
        "headline_top": "5 OBJETOS QUE USAS A DIARIO",
        "headline_bottom": "Y NO CONOCES SU SECRETO",
        "category": "OBJETOS COTIDIANOS",
        "description": "Ese pequeño agujero o bolsillo en tus cosas tiene un propósito oculto de ingeniería 👖 Descubre el verdadero diseño de lo cotidiano.\n\n#EnigmaIQ #Inventos #Curiosidades #Ingenieria #DatosCuriosos #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. El bolsillo diminuto de tus pantalones vaqueros no se creó para monedas ni encendedores.",
                "p2": "Nació en mil ochocientos setenta y tres durante la fiebre del oro para que los vaqueros protegieran sus delicados relojes de bolsillo.",
                "q1": "blue denim jeans pocket close up",
                "q2": "vintage gold pocket watch ticking retro"
            },
            {
                "num": 2,
                "p1": "Número dos. El pequeño orificio junto a la cerradura en la base de los candados tiene doble función vital.",
                "p2": "Permite drenar el agua de lluvia para evitar el óxido interno y sirve como canal para inyectar aceite lubricante en el mecanismo.",
                "q1": "heavy metal padlock locked fence",
                "q2": "lubricating oil drop mechanical padlock"
            },
            {
                "num": 3,
                "p1": "Número tres. Las tapas de los bolígrafos clásicos BIC tienen un agujero en la punta superior por estricta seguridad médica.",
                "p2": "Si un niño o adulto la traga accidentalmente, ese orificio permite el paso mínimo de aire para evitar una asfixia mortal.",
                "q1": "classic blue ballpoint pen writing paper",
                "q2": "pen cap plastic breathing hole macro"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Las botellas de cerveza se fabrican en vidrio ámbar oscuro o verde por una razón química crucial.",
                "p2": "Bloquean los rayos ultravioleta del sol, los cuales de otra forma descompondrían los ácidos del lúpulo arruinando por completo el sabor.",
                "q1": "amber glass beer bottle condensation cold",
                "q2": "sunlight rays shining through glass bottle"
            },
            {
                "num": 5,
                "p1": "Número cinco. Las pelotas de tenis profesionales son de color amarillo fluorescente por exigencia de la televisión.",
                "p2": "Antes eran blancas, pero en mil novecientos setenta y dos adoptaron este tono brillante para verse nítidas en las transmisiones a color.",
                "q1": "neon yellow tennis ball bouncing court",
                "q2": "vintage color television retro broadcast"
            }
        ]
    },

    # Video 24: Tierra & Clima Extremo Vol 1
    {
        "id": "24_EnigmaIQ_5_Cosas_Vol4",
        "title": "5 Fenómenos de la TIERRA que desafían la lógica ⚡🌊",
        "headline_top": "5 FENÓMENOS DE LA TIERRA",
        "headline_bottom": "QUE DESAFÍAN LA LÓGICA",
        "category": "TIERRA & CLIMA EXTREMO",
        "description": "La Tierra tiene lugares y fenómenos que parecen de otro planeta ⚡ Rayos que caen hacia el espacio y el lago donde nadie puede hundirse.\n\n#EnigmaIQ #Tierra #Clima #Fisica #Curiosidades #Misterios #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. Existen relámpagos gigantescos llamados espectros rojos que no descienden a la Tierra.",
                "p2": "Se disparan hacia arriba en dirección al espacio, alcanzando casi cien kilómetros de altura sobre las tormentas más intensas.",
                "q1": "lightning storm clouds night dramatic",
                "q2": "outer space atmosphere earth red glow"
            },
            {
                "num": 2,
                "p1": "Número dos. En las aguas del Mar Muerto es físicamente imposible que una persona se hunda al fondo.",
                "p2": "Su altísima salinidad del treinta y cuatro por ciento genera una densidad tan elevada que tu cuerpo flota como un corcho sin ningún esfuerzo.",
                "q1": "person floating relaxed dead sea water",
                "q2": "salt crystal formations dead sea shore"
            },
            {
                "num": 3,
                "p1": "Número tres. Al contrario de lo que muestran las películas de aventuras, las arenas movedizas jamás te tragarán por completo.",
                "p2": "La densidad del cuerpo humano es menor que la mezcla de arena y agua, por lo que como máximo quedarás atrapado hasta la cintura.",
                "q1": "quicksand mud walking desert boots",
                "q2": "wet sand sinking slow motion boots"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Bajo ciertas condiciones termodinámicas, el agua hirviendo puede congelarse antes que el agua fría.",
                "p2": "Este fascinante fenómeno físico se conoce como Efecto Mpemba y ha desconcertado a científicos desde los tiempos de Aristóteles.",
                "q1": "boiling water thrown freezing air snow",
                "q2": "frost ice crystals growing cold surface"
            },
            {
                "num": 5,
                "p1": "Número cinco. El Punto Nemo en mitad del océano Pacífico es el lugar más inaccesible y solitario de todo el planeta.",
                "p2": "Está tan alejado de tierra firme que los seres humanos más cercanos a ti suelen ser los astronautas de la Estación Espacial Internacional.",
                "q1": "isolated deep pacific ocean waves stormy",
                "q2": "satellite orbiting earth space station"
            }
        ]
    },

    # Video 25: Ingeniería & Aviones Vol 1
    {
        "id": "25_EnigmaIQ_5_Cosas_Vol5",
        "title": "5 Secretos de AVIONES y TRENES que nunca te dijeron ✈️🚄",
        "headline_top": "5 SECRETOS DE AVIONES",
        "headline_bottom": "QUE NUNCA TE DIJERON",
        "category": "INGENIERÍA & TRANSPORTE",
        "description": "La ingeniería aeronáutica y ferroviaria oculta secretos fascinantes ✈️ ¿Por qué todos los aviones son blancos y las ruedas de tren cónicas?\n\n#EnigmaIQ #Aviones #Trenes #Ingenieria #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. Casi todos los aviones comerciales de pasajeros se pintan predominantemente de color blanco.",
                "p2": "Esto refleja el calor de la radiación solar para enfriar la cabina y facilita la detección inmediata de fisuras o fugas en el fuselaje.",
                "q1": "commercial white passenger airplane runway",
                "q2": "airplane wing reflection bright sun flight"
            },
            {
                "num": 2,
                "p1": "Número dos. Las ruedas de acero de los trenes no son cilindros planos, sino que tienen forma cónica inclinada.",
                "p2": "Esa inclinación geométrica hace que los vagones se autocentren solos en las vías al tomar curvas a alta velocidad sin descarrilar jamás.",
                "q1": "train steel wheels rolling on tracks",
                "q2": "high speed modern passenger train railway"
            },
            {
                "num": 3,
                "p1": "Número tres. Si todos los cables de soporte de un ascensor moderno se cortaran a la vez, la cabina no caería al fondo.",
                "p2": "Cuenta con potentes frenos mecánicos de cuña que se clavan automáticamente contra los rieles laterales al detectar exceso de velocidad.",
                "q1": "modern glass elevator shaft steel cables",
                "q2": "heavy industrial metal brake friction"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Las ventanillas de los aviones tienen un diminuto agujero en la parte inferior del panel central de acrílico.",
                "p2": "Es una válvula de escape llamada respiradero que equilibra la gigantesca diferencia de presión entre la cabina y el aire exterior a diez mil metros.",
                "q1": "airplane window passenger seat view",
                "q2": "airplane window hole tiny condensation"
            },
            {
                "num": 5,
                "p1": "Número cinco. Un gigantesco barco carguero construido con miles de toneladas de acero flota gracias al principio de Arquímedes.",
                "p2": "Su enorme casco hueco desplaza un volumen de agua cuyo peso total es superior al de todo el buque y su carga pesada combinados.",
                "q1": "massive container cargo ship ocean waves",
                "q2": "ship hull steel cutting through water"
            }
        ]
    },

    # Video 26: Cuerpo & Sentidos Vol 2
    {
        "id": "26_EnigmaIQ_5_Cosas_Vol6",
        "title": "5 Cosas que tu CUERPO hace sin que te des cuenta 🧠👀",
        "headline_top": "5 COSAS QUE TU CUERPO",
        "headline_bottom": "HACE SIN QUE TE ENTERES",
        "category": "CUERPO HUMANO & MENTE",
        "description": "Tu cuerpo es una máquina biológica alucinante 🧠 Desde por qué se arrugan tus dedos en agua hasta la huella única de tu lengua.\n\n#EnigmaIQ #CuerpoHumano #Salud #Ciencia #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. La piel de tus dedos no se arruga en la ducha porque absorba agua como si fuera una esponja.",
                "p2": "Es una respuesta activa de tu sistema nervioso para crear canales de drenaje que mejoran drásticamente el agarre en superficies mojadas.",
                "q1": "wrinkled wet fingers hands bathtub water",
                "q2": "hand gripping wet stone slippery river"
            },
            {
                "num": 2,
                "p1": "Número dos. El dolor punzante en la cabeza al comer helado muy rápido es en realidad una señal de alarma vascular.",
                "p2": "El frío extremo enfría bruscamente tu paladar, dilatando a toda prisa las arterias cerebrales para mantener la temperatura de tu cerebro.",
                "q1": "person eating cold delicious ice cream",
                "q2": "person holding forehead brain freeze pain"
            },
            {
                "num": 3,
                "p1": "Número tres. Bostezar no solo significa que tienes sueño, sino que funciona como un sistema de refrigeración biológico.",
                "p2": "Al inhalar aire fresco y estirar la mandíbula, tu cuerpo reduce la temperatura de la sangre que irriga directamente las neuronas de tu cerebro.",
                "q1": "person yawning tired desk work morning",
                "q2": "thermal heat map brain scan fMRI"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Al igual que las yemas de tus dedos, la superficie de tu lengua posee una huella completamente única en el mundo.",
                "p2": "El patrón de sus papilas gustativas, surcos y textura microscópica no se repite en ningún otro ser humano del planeta.",
                "q1": "human face smiling mouth tongue detail",
                "q2": "fingerprint scan biometric security line"
            },
            {
                "num": 5,
                "p1": "Número cinco. El ojo de un avestruz africana es físicamente más grande y pesado que todo su cerebro entero.",
                "p2": "Esta asombrosa adaptación evolutiva le permite divisar depredadores a kilómetros de distancia en la sabana abierta antes de que puedan acercarse.",
                "q1": "ostrich head big eyes looking camera",
                "q2": "ostrich running wild savanna desert"
            }
        ]
    },

    # Video 27: Espacio & Cosmos Vol 1
    {
        "id": "27_EnigmaIQ_5_Cosas_Vol7",
        "title": "5 Misterios del ESPACIO que parecen imposibles 🚀🌌",
        "headline_top": "5 MISTERIOS DEL ESPACIO",
        "headline_bottom": "QUE PARECEN IMPOSIBLES",
        "category": "UNIVERSO & ASTRONOMÍA",
        "description": "El espacio exterior desafía todo lo que conocemos 🚀 En Venus un día dura más que un año y los astronautas crecen en órbita.\n\n#EnigmaIQ #Espacio #Cosmos #NASA #Astronomia #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. Al vivir en la ingravidez del espacio, los astronautas regresan a la Tierra siendo más altos que antes.",
                "p2": "Sin la gravedad comprimiendo su cuerpo, los discos vertebrales se expanden permitiéndoles crecer hasta cinco centímetros durante su misión.",
                "q1": "astronaut floating inside space station zero gravity",
                "q2": "human spine vertebrae skeleton expansion 3d"
            },
            {
                "num": 2,
                "p1": "Número dos. En el infernal planeta Venus, un solo día dura mucho más tiempo que todo su año solar completo.",
                "p2": "Tarda doscientos cuarenta y tres días terrestres en girar sobre su propio eje, pero solo doscientos veinticinco en completar su órbita alrededor del Sol.",
                "q1": "planet venus rotating atmosphere space",
                "q2": "sun bright solar flares space orbit"
            },
            {
                "num": 3,
                "p1": "Número tres. Al regresar de una caminata espacial en el vacío, los trajes de los astronautas despiden un olor muy peculiar.",
                "p2": "Huelen a carne asada chamuscada, metal recalentado y humo de soldadura debido a la oxidación de átomos de oxígeno atrapados en la tela.",
                "q1": "spacewalk astronaut outside spacecraft earth",
                "q2": "welding metal sparks industrial hot smoke"
            },
            {
                "num": 4,
                "p1": "Número cuatro. La Luna no se mantiene a una distancia fija, sino que se aleja lentamente de nuestro planeta cada año.",
                "p2": "Debido a la fricción gravitatoria de las mareas oceánicas terrestres, retrocede unos tres coma ocho centímetros anuales hacia el espacio profundo.",
                "q1": "full moon glowing dark night sky telescope",
                "q2": "earth and moon orbiting space dark"
            },
            {
                "num": 5,
                "p1": "Número cinco. Si dos piezas de metal pulido del mismo elemento se tocan en el vacío absoluto del espacio, se fusionan al instante.",
                "p2": "Este proceso se llama soldadura en frío y ocurre porque los átomos metálicos no tienen capas de aire u óxido que los mantengan separados.",
                "q1": "two metal rods touching friction welding",
                "q2": "satellite metallic repair outer space orbit"
            }
        ]
    },

    # Video 28: Historia & Curiosidades Ocultas Vol 1
    {
        "id": "28_EnigmaIQ_5_Cosas_Vol8",
        "title": "5 Mentiras HISTÓRICAS que todo el mundo sigue creyendo 🏛️⚔️",
        "headline_top": "5 MENTIRAS HISTÓRICAS QUE",
        "headline_bottom": "TODOS SIGUEN CREYENDO",
        "category": "HISTORIA OCULTA",
        "description": "La historia no siempre es como nos la contaron 🏛️ Los vikingos jamás usaron cuernos y el ketchup se inventó como jarabe medicinal.\n\n#EnigmaIQ #Historia #Mitos #Curiosidades #XpressTV #DatosCuriosos",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. Los temibles guerreros vikingos jamás llevaron cascos con cuernos en ninguna de sus batallas reales.",
                "p2": "Esa imagen fue un invento teatral del siglo diecinueve diseñado por el vestuarista de la famosa ópera del compositor Richard Wagner.",
                "q1": "viking warrior bearded ship shore historical",
                "q2": "classical opera stage theater actors historical"
            },
            {
                "num": 2,
                "p1": "Número dos. En el año mil ochocientos treinta y cuatro, la salsa de kétchup se vendía formalmente en farmacias como medicina.",
                "p2": "Un médico estadounidense la patentó en forma de píldoras concentradas de tomate asegurando que curaba la diarrea y el cólera.",
                "q1": "tomato ketchup pouring red delicious",
                "q2": "vintage pharmacy medicine glass bottles retro"
            },
            {
                "num": 3,
                "p1": "Número tres. Las zanahorias originales no eran de color naranja, sino moradas, blancas y de un tono amarillo pálido.",
                "p2": "Fueron agricultores holandeses del siglo diecisiete quienes cruzaron cepas para crear la variedad naranja en tributo a la dinastía real de Orange.",
                "q1": "purple and yellow fresh heritage carrots",
                "q2": "fresh orange carrots harvest garden soil"
            },
            {
                "num": 4,
                "p1": "Número cuatro. En la época de los faraones, las grandes pirámides de Guiza no lucían con el aspecto arenoso de hoy.",
                "p2": "Estaban revestidas de finos bloques de piedra caliza blanca perfectamente pulida que reflejaban la luz solar como gigantescos espejos dorados.",
                "q1": "great pyramids giza desert egypt golden",
                "q2": "white limestone polished marble building sun"
            },
            {
                "num": 5,
                "p1": "Número cinco. La guerra más corta registrada en toda la historia de la humanidad duró escasos treinta y ocho minutos.",
                "p2": "Ocurrió en mil ochocientos noventa y seis cuando la armada británica bombardeó el palacio del sultán de Zanzíbar, quien se rindió de inmediato.",
                "q1": "antique naval cannon firing smoke sea",
                "q2": "old historical battleship sailing smoke 1800s"
            }
        ]
    },

    # Video 29: Comida & Química Asombrosa Vol 1
    {
        "id": "29_EnigmaIQ_5_Cosas_Vol9",
        "title": "5 Secretos de la COMIDA que cambiarán cómo comes 🍯🍿",
        "headline_top": "5 SECRETOS DE LA COMIDA",
        "headline_bottom": "QUE TE SORPRENDERÁN",
        "category": "COMIDA & QUÍMICA",
        "description": "Lo que comes todos los días es pura química asombrosa 🍯 La miel nunca caduca y las manzanas flotan por una razón oculta.\n\n#EnigmaIQ #Comida #Cocina #Quimica #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. La miel pura de abeja es el único alimento natural conocido que prácticamente jamás se descompone ni caduca.",
                "p2": "Arqueólogos en Egipto han abierto vasijas selladas en tumbas faraónicas con más de tres mil años y su miel seguía perfectamente comestible.",
                "q1": "golden honey dripping from wooden dipper",
                "q2": "ancient egyptian tomb hieroglyphs desert"
            },
            {
                "num": 2,
                "p1": "Número dos. Las palomitas de maíz estallan porque guardan en su interior una diminuta gota de agua líquida rodeada de almidón duro.",
                "p2": "Al calentarse, el agua se transforma en vapor a altísima presión hasta que revienta la cáscara expandiendo el almidón blanco en milésimas de segundo.",
                "q1": "popcorn popping slow motion machine cinema",
                "q2": "corn kernels yellow macro cooking pot"
            },
            {
                "num": 3,
                "p1": "Número tres. La sensación de picante en tu boca al morder un chile no es un sabor, sino una ilusión de calor y dolor físico.",
                "p2": "La capsaicina engaña a los receptores nerviosos que detectan quemaduras térmicas, haciendo creer a tu cerebro que tu lengua se está incendiando.",
                "q1": "fresh red chili peppers spicy cooking",
                "q2": "flames fire burning heat slow motion"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Si arrojas una manzana fresca a un balde lleno de agua notarás que flota inmediatamente en la superficie.",
                "p2": "Esto se debe a que casi un veinticinco por ciento del volumen total de su carne interna está compuesto por diminutas bolsas de aire.",
                "q1": "red apples floating fresh water bowl splash",
                "q2": "fresh apple orchard picking red apples"
            },
            {
                "num": 5,
                "p1": "Número cinco. En las civilizaciones maya y azteca, los granos de cacao eran tan valiosos que funcionaban literalmente como moneda de cambio.",
                "p2": "Con cuatro semillas podías comprar calabazas frescas y con cien semillas podías pagar por un conejo entero o un sirviente temporal.",
                "q1": "dark chocolate melting smooth liquid rich",
                "q2": "cacao pod beans harvest tropical tree"
            }
        ]
    },

    # Video 30: Selva, Árboles & Naturaleza Viva Vol 1
    {
        "id": "30_EnigmaIQ_5_Cosas_Vol10",
        "title": "5 Cosas que las PLANTAS hacen en secreto 🌿🌳",
        "headline_top": "5 SECRETOS DE LAS PLANTAS",
        "headline_bottom": "QUE PARECEN IMPOSIBLES",
        "category": "BOTÁNICA & NATURALEZA",
        "description": "Las plantas están más vivas de lo que crees 🌿 Se comunican bajo tierra y algunas pueden crecer casi un metro en un solo día.\n\n#EnigmaIQ #Plantas #Naturaleza #Bosque #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. Los árboles de un bosque no compiten ciegamente, sino que se comunican activamente bajo tierra a través de raíces y hongos.",
                "p2": "Esta red micorriza llamada Wood Wide Web les permite advertirse de plagas inminentes y transferirse agua o azúcares a ejemplares enfermos.",
                "q1": "deep green forest canopy trees sunlight",
                "q2": "underground tree roots soil macro detail"
            },
            {
                "num": 2,
                "p1": "Número dos. El bambú gigante posee el récord mundial Guinnes como la planta leñosa con el crecimiento más veloz del planeta.",
                "p2": "Bajo las condiciones adecuadas de humedad tropical puede llegar a crecer hasta noventa centímetros en un solo periodo de veinticuatro horas.",
                "q1": "tall green bamboo forest wind blowing",
                "q2": "fast time lapse plant sprout growing soil"
            },
            {
                "num": 3,
                "p1": "Número tres. La famosa planta carnívora venus atrapamoscas posee una rudimentaria memoria a corto plazo que le permite contar estímulos.",
                "p2": "Para no gastar energía en vano con gotas de lluvia, solo cierra sus hojas con fuerza si un insecto toca dos pelos sensitivos seguidos.",
                "q1": "venus flytrap catching fly macro closing",
                "q2": "insect walking green plant trap garden"
            },
            {
                "num": 4,
                "p1": "Número cuatro. El árbol manzanillo de la muerte en el Caribe es tan venenoso que refugiarse bajo su copa durante una tormenta puede ser letal.",
                "p2": "Las gotas de lluvia disuelven las toxinas cáusticas de su corteza y hojas, cayendo sobre tu piel como si fuera ácido altamente corrosivo.",
                "q1": "heavy rain drops dripping from green leaves",
                "q2": "tropical poisonous tree danger sign forest"
            },
            {
                "num": 5,
                "p1": "Número cinco. El inconfundible y agradable aroma a pasto recién cortado es en realidad un grito químico desesperado de auxilio biológico.",
                "p2": "Al ser podadas, las briznas de hierba liberan compuestos orgánicos volátiles para alertar a plantas vecinas y atraer avispas cazadoras de orugas.",
                "q1": "fresh green lawn grass lawnmower cutting",
                "q2": "green grass meadow morning dew sunrise"
            }
        ]
    },

    # Video 31: Océanos & Criaturas Abisales Vol 1
    {
        "id": "31_EnigmaIQ_5_Cosas_Vol11",
        "title": "5 Secretos de los OCÉANOS que te darán escalofríos 🌊🦑",
        "headline_top": "5 SECRETOS DE LOS OCÉANOS",
        "headline_bottom": "QUE TE DARÁN ESCALOFRÍOS",
        "category": "ABISMOS Y OCÉANOS",
        "description": "Las profundidades del océano son más desconocidas que la Luna 🌊 Descubre criaturas con ojos gigantes y la fosa más profunda de la Tierra.\n\n#EnigmaIQ #Oceano #MisteriosMarinos #Animales #Curiosidades #Ciencia #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. El calamar gigante posee los ojos más grandes de cualquier criatura viviente en todo el reino animal.",
                "p2": "Pueden medir hasta treinta centímetros de diámetro, el tamaño de un balón de baloncesto, diseñados para captar siluetas en la penumbra abisal.",
                "q1": "giant squid deep dark ocean underwater",
                "q2": "glowing bioluminescent creatures deep sea"
            },
            {
                "num": 2,
                "p1": "Número dos. En el fondo de la Fosa de las Marianas, a once kilómetros bajo el nivel del mar, la presión es aplastante.",
                "p2": "Supera las mil atmósferas, equivalente a tener el peso descomunal de cincuenta aviones jumbo apoyados sobre tu cabeza.",
                "q1": "deep sea submarine exploration dark abyss",
                "q2": "underwater trench rocky deep sea exploration"
            },
            {
                "num": 3,
                "p1": "Número tres. La gran mayoría de los peces que habitan en la zona abisal producen su propia luz en la oscuridad.",
                "p2": "Utilizan reacciones químicas de bioluminiscencia y bacterias simbióticas para comunicarse, atraer presas desprevenidas o camuflarse de cazadores.",
                "q1": "bioluminescent anglerfish glowing dark underwater",
                "q2": "deep ocean glowing jellyfish pulsing"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Más de la mitad del oxígeno que respiras a diario en el planeta no proviene de los bosques amazónicos.",
                "p2": "Es producido por miles de millones de microorganismos marinos fotosintéticos conocidos colectivamente como fitoplancton en los océanos.",
                "q1": "ocean phytoplankton turquoise swirling waves satellite",
                "q2": "sunbeams underwater clear ocean water"
            },
            {
                "num": 5,
                "p1": "Número cinco. Existe una masa flotante de desechos plásticos en el Pacífico norte que triplica la superficie de toda Francia.",
                "p2": "Las corrientes marinas en remolino concentran millones de toneladas de microplásticos que amenazan a cientos de especies marinas migratorias.",
                "q1": "plastic pollution floating in blue ocean",
                "q2": "sea turtle swimming ocean underwater coral"
            }
        ]
    },

    # Video 32: Tecnología Antigua & Mecanismos Perdidos Vol 1
    {
        "id": "32_EnigmaIQ_5_Cosas_Vol12",
        "title": "5 Inventos ANTIGUOS que desafían la historia moderna ⚙️🏛️",
        "headline_top": "5 INVENTOS ANTIGUOS QUE",
        "headline_bottom": "DESAFÍAN LA HISTORIA",
        "category": "TECNOLOGÍA ANTIGUA",
        "description": "Los antiguos tenían tecnología mucho más avanzada de lo que nos contaron ⚙️ Computadoras griegas de bronce y concreto romano autorreparable.\n\n#EnigmaIQ #Historia #Arqueologia #Inventos #Misterios #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. El mecanismo de Anticitera es considerado la primera computadora analógica mecánica de toda la humanidad.",
                "p2": "Construido en la antigua Grecia hace más de dos mil años con más de treinta engranajes de bronce, predecía eclipses lunares y solares con precisión milimétrica.",
                "q1": "ancient bronze gears mechanism antique clockwork",
                "q2": "ancient greek temple ruins sunny acropolis"
            },
            {
                "num": 2,
                "p1": "Número dos. El temible fuego griego fue un arma incendiaria bizantina cuya fórmula química jamás pudo ser descifrada.",
                "p2": "Se disparaba a través de sifones sobre barcos enemigos y tenía la aterradora propiedad de seguir ardiendo con mayor furia sobre el agua marina.",
                "q1": "flames burning water naval battle historical",
                "q2": "ancient wooden warship naval fire"
            },
            {
                "num": 3,
                "p1": "Número tres. Los acueductos y edificios romanos siguen en pie después de dos mil años gracias a su concreto autorreparable.",
                "p2": "Al mezclar cal viva con ceniza volcánica, cuando una grieta se forma y entra agua de lluvia, la cal se disuelve y sella la fisura químicamente.",
                "q1": "ancient roman colosseum aqueduct sunny historical",
                "q2": "cracked stone concrete wall macro repair"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Las legendarias espadas forjadas con acero de Damasco poseían una resistencia y filo casi sobrenaturales.",
                "p2": "Análisis modernos revelaron que los herreros medievales creaban sin saberlo nanotubos de carbono y nanocables de hierro durante el forjado a fuego.",
                "q1": "blacksmith forging glowing red hot sword hammer",
                "q2": "damascus steel blade pattern closeup sharp"
            },
            {
                "num": 5,
                "p1": "Número cinco. Las misteriosas vasijas de Bagdad sugieren que en la antigua Mesopotamia ya conocían principios de electroquímica.",
                "p2": "Consistían en jarras de arcilla con cilindros de cobre y varillas de hierro que al llenarse con vinagre o zumo ácido generaban pequeñas corrientes eléctricas.",
                "q1": "ancient clay pottery museum artifact middle east",
                "q2": "electrical spark battery current macro physics"
            }
        ]
    },

    # Video 33: Psicología Humana & Ilusiones Mentales Vol 1
    {
        "id": "33_EnigmaIQ_5_Cosas_Vol13",
        "title": "5 Trucos de tu CEREBRO que controlan lo que piensas 🧠🎭",
        "headline_top": "5 TRUCOS DE TU CEREBRO",
        "headline_bottom": "QUE CONTROLAN TU MENTE",
        "category": "PSICOLOGÍA & MENTE",
        "description": "Tu mente te engaña constantemente sin que te des cuenta 🧠 Desde el misterioso Efecto Mandela hasta la parálisis del sueño.\n\n#EnigmaIQ #Psicologia #Cerebro #Mente #Curiosidades #Ciencia #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. El Efecto Mandela es un fenómeno donde millones de personas comparten un recuerdo histórico completamente falso.",
                "p2": "Desde el monóculo que el muñeco de Monopoly jamás tuvo hasta frases célebres de películas que los personajes nunca llegaron a pronunciar.",
                "q1": "crowd of people walking city street blur",
                "q2": "brain synapses firing neurons mental thought"
            },
            {
                "num": 2,
                "p1": "Número dos. Cuando aprendes una palabra nueva o compras un auto y comienzas a verlo en todas partes, tu cerebro te está engañando.",
                "p2": "Se llama ilusión de frecuencia o fenómeno Baader-Meinhof, un sesgo de atención selectiva donde tu mente prioriza información reciente.",
                "q1": "person reading book in library thinking",
                "q2": "traffic cars street urban city daylight"
            },
            {
                "num": 3,
                "p1": "Número tres. La aterradora parálisis del sueño ocurre cuando tu mente despierta antes de que tu cerebro reactive tus músculos.",
                "p2": "Durante la fase REM el cuerpo segrega glicina para inmovilizarte y no actuar físicamente tus sueños; si ese freno falla unos segundos, quedas consciente e inmóvil.",
                "q1": "person waking up bedroom dark shadow fear",
                "q2": "clock ticking bedside table night darkness"
            },
            {
                "num": 4,
                "p1": "Número cuatro. La extraña sensación de déjà vu no es una premonición sobrenatural ni una vida pasada.",
                "p2": "Es un microscópico retraso neurológico en el que una parte de tu cerebro procesa la información presente como si ya estuviera almacenada en tu memoria a largo plazo.",
                "q1": "person looking confused mirror reflection",
                "q2": "hourglass sand flowing slow motion time"
            },
            {
                "num": 5,
                "p1": "Número cinco. El efecto placebo es tan poderoso que tu organismo puede curarse con pastillas de azúcar vacías.",
                "p2": "La simple creencia de estar recibiendo un tratamiento efectivo activa la liberación de dopamina y endorfinas analgésicas reales en tu sistema nervioso.",
                "q1": "doctor holding medical pill capsule prescription",
                "q2": "patient smiling relief recovery clinic"
            }
        ]
    },

    # Video 34: Animales con Superpoderes Vol 2
    {
        "id": "34_EnigmaIQ_5_Cosas_Vol14",
        "title": "5 Animales con SUPERPODERES que humillan a la ciencia 🦹🐾",
        "headline_top": "5 ANIMALES CON PODERES",
        "headline_bottom": "QUE PARECEN MUTANTES",
        "category": "SUPER ANIMALES",
        "description": "La evolución creó criaturas con habilidades dignas de superhéroes 🦹 Desde seres inmortales hasta golpes que alcanzan la temperatura solar.\n\n#EnigmaIQ #Animales #Superpoderes #Naturaleza #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. Los microscópicos tardígrados u osos de agua son prácticamente indestructibles ante cualquier catástrofe.",
                "p2": "Pueden sobrevivir al vacío del espacio, a la radiación cósmica letal y a temperaturas de doscientos grados bajo cero expulsando el agua de su cuerpo.",
                "q1": "water bear tardigrade microscopic extreme closeup",
                "q2": "outer space stars deep galaxy nebula"
            },
            {
                "num": 2,
                "p1": "Número dos. La diminuta medusa Turritopsis dohrnii es el único ser vivo biológicamente inmortal del planeta.",
                "p2": "Cuando envejece o sufre estrés extremo, revierte todas sus células adultas a su fase inicial de pólipo infantil reiniciando su ciclo de vida infinitamente.",
                "q1": "translucent jellyfish floating deep blue ocean",
                "q2": "glowing underwater marine life pulsing"
            },
            {
                "num": 3,
                "p1": "Número tres. El camarón pistola posee una de las armas de caza biológicas más letales y rápidas de la Tierra.",
                "p2": "Al cerrar su pinza a cien kilómetros por hora crea una burbuja de cavitación cuya implosión alcanza cuatro mil grados centígrados, casi la superficie del Sol.",
                "q1": "pistol shrimp colorful claws underwater reef",
                "q2": "shockwave explosion bubble water splash macro"
            },
            {
                "num": 4,
                "p1": "Número cuatro. El ornitorrinco es uno de los mamíferos más extraños por combinar habilidades anatómicas únicas.",
                "p2": "Pone huevos, detecta los campos eléctricos de sus presas bajo el fango con su pico de pato y los machos poseen espolones con potente veneno en sus patas.",
                "q1": "platypus swimming freshwater river underwater",
                "q2": "australian wild river creek tropical nature"
            },
            {
                "num": 5,
                "p1": "Número cinco. El ajolote mexicano posee una capacidad de regeneración celular tan asombrosa que parece pura magia médica.",
                "p2": "Puede regenerar extremidades amputadas, partes de su corazón, médula espinal e incluso fragmentos de su cerebro sin dejar cicatrices visibles.",
                "q1": "pink axolotl smiling freshwater aquarium closeup",
                "q2": "clean freshwater plants underwater tank"
            }
        ]
    },

    # Video 35: El Planeta Tierra & Clima Inexplicable Vol 2
    {
        "id": "35_EnigmaIQ_5_Cosas_Vol15",
        "title": "5 Lugares de la TIERRA que parecen de otro PLANETA 🌋❄️",
        "headline_top": "5 LUGARES DE LA TIERRA",
        "headline_bottom": "QUE PARECEN ALIENÍGENAS",
        "category": "MARAVILLAS DEL PLANETA",
        "description": "Lugares reales en nuestro planeta que desafían la imaginación 🌋 Rayos perpetuos, cristales gigantes y lagos que petrifican.\n\n#EnigmaIQ #LugaresExtremos #Tierra #Viajes #Misterios #Naturaleza #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. En la desembocadura del río Catatumbo en Venezuela ocurre la tormenta eléctrica más constante y duradera del mundo.",
                "p2": "Durante casi trescientas noches al año se desatan hasta doscientos cincuenta relámpagos por hora en silencio absoluto iluminando todo el horizonte nocturno.",
                "q1": "catatumbo lightning night thunderstorm lake",
                "q2": "dramatic electric storm night sky flash"
            },
            {
                "num": 2,
                "p1": "Número dos. En la Cueva de los Cristales de Naica en México se hallan columnas de selenita de más de diez metros de longitud.",
                "p2": "A trescientos metros de profundidad y con cincuenta grados de calor húmedo, un humano solo puede sobrevivir diez minutos dentro sin equipo de refrigeración.",
                "q1": "massive giant crystals cave exploration underground",
                "q2": "explorer in protective suit hot cave crystals"
            },
            {
                "num": 3,
                "p1": "Número tres. El inquietante lago Natrón en Tanzania tiene aguas tan alcalinas y ricas en carbonato sódico que petrifica animales.",
                "p2": "Cualquier ave desorientada que caiga en sus aguas rojizas muere y queda calcificada lentamente como una estatua de sal inmortalizada en la orilla.",
                "q1": "red salty lake aerial landscape africa",
                "q2": "petrified dead tree branches salty shore"
            },
            {
                "num": 4,
                "p1": "Número cuatro. En el corazón del desierto de Atacama en Chile existen zonas áridas donde jamás se ha registrado una sola gota de lluvia.",
                "p2": "Es el desierto no polar más seco de la Tierra, con condiciones tan extremas que la NASA prueba allí sus robots destinados a buscar vida en Marte.",
                "q1": "dry barren atacama desert sand mountains",
                "q2": "mars rover vehicle testing rocky desert"
            },
            {
                "num": 5,
                "p1": "Número cinco. Las fascinantes auroras boreales del Círculo Polar Ártico son el resultado visual de una colisión cósmica constante.",
                "p2": "Partículas cargadas expulsadas por el viento solar chocan a millones de kilómetros por hora contra los gases nobles del campo magnético terrestre.",
                "q1": "northern lights aurora borealis green purple night sky",
                "q2": "snowy arctic landscape illuminated green aurora"
            }
        ]
    },

    # Video 36: Secretos Militares & Espionaje Insólito Vol 1
    {
        "id": "36_EnigmaIQ_5_Cosas_Vol16",
        "title": "5 Secretos de ESPIONAJE militar que fueron desclasificados 🕵️‍♂️📜",
        "headline_top": "5 SECRETOS DE ESPIONAJE",
        "headline_bottom": "QUE PARECEN DE PELÍCULA",
        "category": "SECRETOS DE GUERRA",
        "description": "Planes militares reales de espionaje que la CIA y ejércitos intentaron ocultar 🕵️‍♂️ Desde gatos cyborg espías hasta palomas con cámaras aéreas.\n\n#EnigmaIQ #Espionaje #HistoriaMilitar #Secretos #CIA #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. En la década de mil novecientos sesenta, la CIA gastó millones de dólares en la insólita Operación Acoustic Kitty.",
                "p2": "Cirujanos implantaron micrófonos y baterías dentro de un gato para espiar a diplomáticos soviéticos, pero el felino fue atropellado en su primera misión.",
                "q1": "cat walking urban street city pavement",
                "q2": "vintage audio microphone wiretap surveillance"
            },
            {
                "num": 2,
                "p1": "Número dos. Durante la Primera Guerra Mundial, el ejército alemán entrenó palomas mensajeras con cámaras fotográficas automáticas en el pecho.",
                "p2": "Las aves sobrevolaban las trincheras enemigas activando temporizadores mecánicos que tomaban fotografías aéreas espía de alta nitidez.",
                "q1": "pigeon bird flying blue sky wings",
                "q2": "aerial black and white vintage reconnaissance photo"
            },
            {
                "num": 3,
                "p1": "Número tres. El famoso psicólogo B. F. Skinner diseñó durante la guerra el Proyecto Paloma para guiar misiles antibuque.",
                "p2": "Entrenó palomas dentro de las ojivas para picotear una pantalla al ver la silueta del barco enemigo corrigiendo la trayectoria de vuelo en caída libre.",
                "q1": "military missile launching naval ship ocean",
                "q2": "pigeon pecking seeds laboratory experiment"
            },
            {
                "num": 4,
                "p1": "Número cuatro. La legendaria máquina de cifrado nazi Enigma se consideraba matemáticamente inexpugnable e indescifrable.",
                "p2": "Sin embargo, el genio matemático Alan Turing y su equipo en Bletchley Park construyeron la máquina Bombe descifrando miles de mensajes vitales diarios.",
                "q1": "antique enigma code machine brass keys cipher",
                "q2": "vintage computer relays spinning mathematical code"
            },
            {
                "num": 5,
                "p1": "Número cinco. La ciudad secreta de Oak Ridge en Tennessee albergó a más de setenta y cinco mil personas sin aparecer en ningún mapa oficial.",
                "p2": "Sus habitantes trabajaban día y noche separando uranio enriquecido para el Proyecto Manhattan sin saber para qué se usaría hasta el final de la guerra.",
                "q1": "industrial factory smoke pipes vintage 1940s",
                "q2": "atomic nuclear laboratory testing equipment vintage"
            }
        ]
    },

    # Video 37: Invenciones Accidentales & Casualidades Vol 1
    {
        "id": "37_EnigmaIQ_5_Cosas_Vol17",
        "title": "5 Inventos MILLONARIOS que nacieron por un puro ERROR 💡💥",
        "headline_top": "5 INVENTOS MILLONARIOS",
        "headline_bottom": "QUE NACIERON POR ACCIDENTE",
        "category": "INVENTOS CASUALES",
        "description": "Grandes inventos que cambiaron el mundo y nacieron de un error en el laboratorio 💡 El horno microondas y la penicilina que salvó millones de vidas.\n\n#EnigmaIQ #Inventos #Ciencia #Descubrimientos #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. El horno microondas que usas a diario fue descubierto cuando una barra de chocolate se derritió en un bolsillo.",
                "p2": "El ingeniero Percy Spencer estaba probando un radar militar de magnetrón cuando notó que las ondas electromagnéticas calentaban la comida al instante.",
                "q1": "modern kitchen microwave oven heating food",
                "q2": "chocolate melting smooth hot liquid drip"
            },
            {
                "num": 2,
                "p1": "Número dos. La penicilina, el primer antibiótico moderno de la humanidad, nació gracias al descuido de un científico desordenado.",
                "p2": "Alexander Fleming se fue de vacaciones y dejó placas de bacterias abiertas; al volver, descubrió que un hongo verde había aniquilado a todos los microbios.",
                "q1": "scientist looking through laboratory microscope",
                "q2": "petri dish bacteria mold fungus growth lab"
            },
            {
                "num": 3,
                "p1": "Número tres. Las famosas notas adhesivas amarillas Post-it surgieron de un intento completamente fallido por crear un pegamento ultra fuerte.",
                "p2": "El adhesivo resultó ser tan débil que podía despegarse y pegarse una y otra vez sin romper las hojas ni dejar residuos pegajosos en el papel.",
                "q1": "yellow sticky notes attached wall message office",
                "q2": "hand peeling sticky note paper desk"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Alfred Nobel inventó la dinamita por pura casualidad al intentar hacer más segura la peligrosa nitroglicerina líquida.",
                "p2": "Descubrió que al mezclar el explosivo inestable con tierra fosilífera porosa se formaba una pasta moldeable que solo detonaba con mecha controlada.",
                "q1": "quarry explosion rocks blasting dust slow motion",
                "q2": "sticks of vintage dynamite with fuse wire"
            },
            {
                "num": 5,
                "p1": "Número cinco. El teflón antiadherente de tus sartenes fue hallado accidentalmente por el químico Roy Plunkett en un laboratorio.",
                "p2": "Al abrir un cilindro congelado de gas refrigerante vio que el gas se había polimerizado en una sustancia resbaladiza e inmune a químicos corrosivos.",
                "q1": "frying pan cooking egg sliding non stick",
                "q2": "industrial chemistry laboratory experiment testing"
            }
        ]
    },

    # Video 38: El Universo Profundo & Agujeros Negros Vol 2
    {
        "id": "38_EnigmaIQ_5_Cosas_Vol18",
        "title": "5 Horrores del ESPACIO PROFUNDO que la NASA vigila 🕳️🌌",
        "headline_top": "5 HORRORES DEL ESPACIO",
        "headline_bottom": "QUE LA NASA VIGILA",
        "category": "COSMOS & AGUJEROS NEGROS",
        "description": "El cosmos guarda fenómenos tan extremos que desafían la física conocida 🕳️ Agujeros negros que detienen el tiempo y estrellas que pesan billones.\n\n#EnigmaIQ #Espacio #AgujeroNegro #NASA #Astronomia #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. Alrededor de un agujero negro existe una frontera invisible conocida como horizonte de sucesos.",
                "p2": "Una vez que la cruzas, nada ni siquiera la luz que viaja a trescientos mil kilómetros por segundo puede escapar de su atracción gravitatoria eterna.",
                "q1": "massive black hole event horizon accretion disk",
                "q2": "space vortex gravity bending light warp"
            },
            {
                "num": 2,
                "p1": "Número dos. Si un astronauta cayera en las cercanías de un agujero negro sufriría un proceso real llamado espaguetización.",
                "p2": "La gravedad en sus pies sería infinitamente más intensa que en su cabeza, estirando su cuerpo como un fideo kilométrico en cuestión de segundos.",
                "q1": "astronaut floating deep space nebula starfield",
                "q2": "distortion warp space time theoretical physics"
            },
            {
                "num": 3,
                "p1": "Número tres. Las estrellas de neutrones son los objetos astronómicos más densos y compactos conocidos en todo el universo observable.",
                "p2": "Una sola cucharadita de café de su materia comprimida pesaría en la Tierra aproximadamente mil millones de toneladas equivalentes a una montaña entera.",
                "q1": "pulsar neutron star spinning magnetic beams space",
                "q2": "heavy rock mountain landscape aerial clouds"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Nuestra galaxia, la Vía Láctea, viaja en curso de colisión frontal contra la gigantesca galaxia de Andrómeda.",
                "p2": "Ambas chocan a cuatrocientos mil kilómetros por hora y dentro de cuatro mil millones de años se fusionarán para formar una sola supergalaxia.",
                "q1": "milky way galaxy spiral night sky telescope",
                "q2": "andromeda galaxy colliding cosmic simulation"
            },
            {
                "num": 5,
                "p1": "Número cinco. La estática con ruido blanco que sintonizaban las televisiones antiguas contenía un eco real del origen del cosmos.",
                "p2": "Aproximadamente un uno por ciento de esa señal residual correspondía a la radiación cósmica de fondo de microondas liberada durante el mismísimo Big Bang.",
                "q1": "vintage tv screen static white noise grain",
                "q2": "cosmic microwave background radiation map universe"
            }
        ]
    },

    # Video 39: Supersticiones & Orígenes Inesperados Vol 1
    {
        "id": "39_EnigmaIQ_5_Cosas_Vol19",
        "title": "5 Supersticiones que TODA tu familia repite y su origen 🪜🧂",
        "headline_top": "5 SUPERSTICIONES QUE CREES",
        "headline_bottom": "Y SU VERDADERO ORIGEN",
        "category": "SUPERSTICIONES & MITOS",
        "description": "Desde tocar madera hasta no derramar la sal en la mesa 🧂 Descubre el verdadero trasfondo histórico detrás de las supersticiones.\n\n#EnigmaIQ #Mitos #Supersticiones #Historia #Curiosidades #Cultura #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. La popular costumbre de tocar madera para evitar la mala suerte se remonta a los antiguos rituales paganos celtas.",
                "p2": "Ellos creían que los espíritus protectores de la naturaleza habitaban dentro de los robles y que dar golpes a la corteza despertaba su protección mágica.",
                "q1": "hand knocking touching wooden table tree bark",
                "q2": "ancient mystical forest trees fog sunny"
            },
            {
                "num": 2,
                "p1": "Número dos. El mito de que romper un espejo atrae siete largos años de mala suerte nació con los médicos del imperio romano.",
                "p2": "Los romanos creían que el cuerpo y alma humana se renovaban biológicamente en ciclos de siete años, y que un espejo roto dañaba esa renovación espiritual.",
                "q1": "broken shattered glass mirror reflection cracks",
                "q2": "roman ancient ruins statues marble columns"
            },
            {
                "num": 3,
                "p1": "Número tres. La advertencia de jamás pasar por debajo de una escalera no surgió por temor a que te cayera un bote de pintura encima.",
                "p2": "Una escalera apoyada contra la pared forma un triángulo sagrado de la Trinidad, y en la Edad Media caminar a través de él se consideraba sacrilegio.",
                "q1": "wooden ladder leaning against wall alley street",
                "q2": "gothic church cathedral stained glass window"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Creer que derramar sal en la mesa trae ruina económica proviene de los campamentos de los legionarios romanos.",
                "p2": "La sal marina era un condimento tan escaso y preciado que se usaba como pago salarial, por lo que derramarla era literalmente tirar dinero valioso al suelo.",
                "q1": "salt spilling from shaker on wooden table",
                "q2": "ancient roman soldiers armor marching historical"
            },
            {
                "num": 5,
                "p1": "Número cinco. El temor universal al viernes trece tiene su origen documentado en un trágico evento histórico de la Europa medieval.",
                "p2": "El viernes trece de octubre de mil trescientos siete, el rey de Francia ordenó el arresto, tortura y quema en la hoguera de todos los Caballeros Templarios.",
                "q1": "calendar page date 13 friday close up",
                "q2": "knights templar armor sword medieval historical"
            }
        ]
    },

    # Video 40: Récords del Cuerpo Humano Vol 3
    {
        "id": "40_EnigmaIQ_5_Cosas_Vol20",
        "title": "5 Récords de tu CUERPO que no parecen biológicos 🫀⚡",
        "headline_top": "5 RÉCORDS DE TU CUERPO",
        "headline_bottom": "QUE PARECEN IMPOSIBLES",
        "category": "SUPER CUERPO HUMANO",
        "description": "Tu organismo es una maravilla biológica insuperable 🫀 La fuerza de tu mandíbula, tu ácido estomacal y la velocidad de tus neuronas.\n\n#EnigmaIQ #CuerpoHumano #Biologia #Medicina #Ciencia #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. El músculo más potente y con mayor fuerza de presión de todo tu cuerpo en proporción a su tamaño es el masetero.",
                "p2": "Ubicado en tu mandíbula, puede ejercer una fuerza de mordida de hasta noventa kilos sobre los molares suficiente para quebrar frutos secos duros.",
                "q1": "human jaw bone teeth skull anatomy 3d",
                "q2": "person biting apple crisp healthy food"
            },
            {
                "num": 2,
                "p1": "Número dos. Tu corazón es un motor incansable que genera suficiente energía a lo largo de tu vida para viajar ida y vuelta a la Luna.",
                "p2": "Bombea casi ocho mil litros de sangre diarios y en un mes normal impulsa el volumen necesario para llenar un camión cisterna por completo.",
                "q1": "human heart beating pumping blood 3d animation",
                "q2": "tanker truck driving highway highway sunny"
            },
            {
                "num": 3,
                "p1": "Número tres. La córnea transparente de tus ojos es el único tejido vivo de todo el organismo que no tiene ningún vaso sanguíneo.",
                "p2": "Para mantenerse perfectamente lúcida y cristalina no recibe sangre, sino que absorbe el oxígeno directamente del aire que te rodea cada vez que parpadeas.",
                "q1": "human eye iris pupil macro blue closeup",
                "q2": "eye blinking contact lens moisture drops"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Los impulsos eléctricos que viajan por tus neuronas transmiten información a velocidades verdaderamente asombrosas.",
                "p2": "Las señales nerviosas más veloces pueden alcanzar más de cuatrocientos kilómetros por hora superando la velocidad punta de un monoplaza de Fórmula Uno.",
                "q1": "neural network glowing electric brain synapses",
                "q2": "race car speeding fast motion track blur"
            },
            {
                "num": 5,
                "p1": "Número cinco. El ácido clorhídrico concentrado presente en tu estómago es tan potente que podría perforar metales blandos.",
                "p2": "Tu estómago no se disuelve a sí mismo únicamente porque produce una gruesa capa de mucosa protectora que se regenera por completo cada tres días.",
                "q1": "stomach digestive system anatomy medical 3d",
                "q2": "acid reacting metal chemical bubbling liquid"
            }
        ]
    },

    # Video 41: Ciudades Subterráneas & Arquitectura Imposible Vol 1
    {
        "id": "41_EnigmaIQ_5_Cosas_Vol21",
        "title": "5 Megaciudades SUBTERRÁNEAS que se construyeron bajo tierra ⛏️🏰",
        "headline_top": "5 CIUDADES SUBTERRÁNEAS",
        "headline_bottom": "CONSTRUIDAS BAJO TIERRA",
        "category": "ARQUITECTURA & MISTERIOS",
        "description": "Ciudades secretas construidas bajo tierra hace siglos ⛏️ Desde búnkeres gigantes en Turquía hasta catacumbas con millones de esqueletos.\n\n#EnigmaIQ #Historia #Arquitectura #Ciudades #Misterios #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. La misteriosa ciudad subterránea de Derinkuyu en Turquía fue excavada en roca volcánica hace miles de años.",
                "p2": "Descendía dieciocho niveles bajo tierra con pozos de ventilación, iglesias y establos para resguardar a más de veinte mil personas durante invasiones enemigas.",
                "q1": "derinkuyu underground city stone tunnels cappadocia",
                "q2": "ancient stone carved caves torchlight"
            },
            {
                "num": 2,
                "p1": "Número dos. Bajo las elegantes calles y avenidas de París se extiende un laberinto de catacumbas que alberga seis millones de esqueletos.",
                "p2": "Fueron creadas a finales del siglo dieciocho para vaciar los cementerios colapsados de la ciudad apilando cráneos y huesos a lo largo de cientos de kilómetros.",
                "q1": "paris catacombs skulls bones walls dark tunnel",
                "q2": "paris aerial view eiffel tower sunny cityscape"
            },
            {
                "num": 3,
                "p1": "Número tres. La Bóveda Global de Semillas de Svalbard se encuentra excavada en las montañas congeladas del archipiélago ártico de Noruega.",
                "p2": "Diseñada a prueba de bombas nucleares y terremotos extremos, custodia más de un millón de muestras agrícolas para reiniciar la humanidad tras un apocalipsis.",
                "q1": "svalbard seed vault entrance snowy mountain arctic",
                "q2": "seed samples in jars agricultural science lab"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Varias estaciones del metro de Moscú en Rusia fueron construidas a más de ochenta metros de profundidad bajo el suelo.",
                "p2": "Además de parecer palacios de mármol con lámparas de araña, fueron ideadas como refugios nucleares herméticos durante las tensiones de la Guerra Fría.",
                "q1": "moscow metro station grand marble architecture chandeliers",
                "q2": "underground heavy steel blast bunker door"
            },
            {
                "num": 5,
                "p1": "Número cinco. La mina de sal de Wieliczka en Polonia esconde una monumental catedral subterránea esculpida por mineros durante siglos.",
                "p2": "Todo en su interior desde los altares hasta los candelabros colgantes está tallado a mano con sal gema sólida sin ningún tipo de cemento.",
                "q1": "wieliczka salt mine underground chapel chandeliers",
                "q2": "salt crystal formations carved cavern walls"
            }
        ]
    },

    # Video 42: Leyendas Urbanas Científicamente Desmentidas Vol 1
    {
        "id": "42_EnigmaIQ_5_Cosas_Vol22",
        "title": "5 Mentiras que te dijo tu MAESTRA y que la ciencia desmintió 👩‍🏫❌",
        "headline_top": "5 MITOS QUE TE DIJERON",
        "headline_bottom": "Y RESULTARON SER MENTIRA",
        "category": "CIENCIA VS MITOS",
        "description": "Mitos populares que la escuela o tu familia te hicieron creer 👩‍🏫 ¿Usamos el 10% del cerebro? ¿Tragarte un chicle tarda 7 años en salir?\n\n#EnigmaIQ #Ciencia #Mitos #Educacion #Aprender #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. El extendido mito de que los humanos solo utilizamos el diez por ciento de nuestra capacidad cerebral es una falsedad rotunda.",
                "p2": "Las resonancias magnéticas modernas demuestran que utilizamos prácticamente el cien por ciento del cerebro incluso cuando estamos profundamente dormidos.",
                "q1": "brain fMRI scan glowing active regions 3d",
                "q2": "person student studying library focused"
            },
            {
                "num": 2,
                "p1": "Número dos. Tu madre te dijo que si te tragabas un chicle se quedaría pegado en tus intestinos durante siete largos años.",
                "p2": "Aunque su goma sintética no se disuelve, tu sistema digestivo la expulsa naturalmente a través de las heces en menos de cuarenta y ocho horas.",
                "q1": "bubble gum bubble blowing colorful playful",
                "q2": "stomach digestive tract intestines medical 3d"
            },
            {
                "num": 3,
                "p1": "Número tres. La creencia de que una moneda lanzada desde lo alto de un rascacielos puede partir el cráneo de un peatón es físicamente imposible.",
                "p2": "Por su forma plana y resistencia con el aire, alcanza una velocidad terminal de apenas cuarenta kilómetros por hora causándote un leve chichón.",
                "q1": "empire state skyscraper looking down height",
                "q2": "coin falling slow motion hand caught"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Comer muchas zanahorias jamás te dará una visión nocturna sobrehumana en la oscuridad como te dijeron de niño.",
                "p2": "Fue una brillante campaña de propaganda militar británica en la Segunda Guerra Mundial para ocultar a los alemanes su nuevo sistema de radar secreto.",
                "q1": "bunch of fresh orange carrots kitchen table",
                "q2": "radar screen sweep blip military surveillance"
            },
            {
                "num": 5,
                "p1": "Número cinco. El agua del retrete o del lavabo no gira en sentido contrario en el hemisferio sur debido al efecto Coriolis.",
                "p2": "La fuerza Coriolis terrestre es tan diminuta a pequeña escala que la dirección del remolino depende únicamente del diseño y ángulo de los desagües.",
                "q1": "water vortex swirling down sink drain blue",
                "q2": "globe planet earth rotating space geography"
            }
        ]
    },

    # Video 43: Minerales Extraños & Gemas Asombrosas Vol 1
    {
        "id": "43_EnigmaIQ_5_Cosas_Vol23",
        "title": "5 Minerales TAN RAROS que parecen salidos de Avatar 💎🔮",
        "headline_top": "5 MINERALES TAN RAROS",
        "headline_bottom": "QUE PARECEN DE OTRO MUNDO",
        "category": "GEOLOGÍA & MINERALES",
        "description": "Piedras que se mueven solas, lluvia de diamantes en el cosmos y minerales con agua atrapada 💎 La geología de la Tierra y el espacio.\n\n#EnigmaIQ #Minerales #Gemas #Geologia #Tierra #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. En las atmósferas de gigantes gaseosos como Saturno y Neptuno los científicos afirman que llueven diamantes del cielo.",
                "p2": "Las tormentas eléctricas descomponen el metano en carbono, y las brutales presiones planetarias lo comprimen en diamantes sólidos cayendo al núcleo.",
                "q1": "saturn rings planet atmosphere deep space",
                "q2": "shiny sparkling cut diamonds macro sparkle"
            },
            {
                "num": 2,
                "p1": "Número dos. La preciada gema conocida como ópalo esconde en su estructura interna una cantidad asombrosa de agua prehistórica.",
                "p2": "Entre un seis y hasta un veinte por ciento de su peso molecular está compuesto por microesferas de sílice que atrapan moléculas de agua atrapadas por millones de años.",
                "q1": "colorful fire opal gemstone reflecting rainbow lights",
                "q2": "water droplet splashing macro clean"
            },
            {
                "num": 3,
                "p1": "Número tres. Las famosas piedras rodantes del Valle de la Muerte en California se deslizaban por el suelo sin que nadie las empujara.",
                "p2": "El enigma se resolvió al descubrir que en noches heladas se forma una lámina de hielo milimétrica que el viento suave empuja arrastrando las rocas.",
                "q1": "sailing stones death valley desert track dry lake",
                "q2": "thin sheet of ice cracking melting winter"
            },
            {
                "num": 4,
                "p1": "Número cuatro. La magnetita natural fue el primer imán permanente descubierto por los seres humanos en la antigüedad.",
                "p2": "Este mineral de óxido ferroso permitió a los navegantes chinos inventar las primeras brújulas del mundo guiando expediciones transoceánicas.",
                "q1": "natural black magnetite stone magnetic attraction",
                "q2": "antique nautical compass brass ship navigation"
            },
            {
                "num": 5,
                "p1": "Número cinco. El bismuto es un elemento metálico que al cristalizarse crea escaleras geométricas con hipnóticos colores de arcoíris.",
                "p2": "Su óxido superficial crea capas de grosor milimétrico que refractan la luz en tonos violáceos, turquesas y dorados que parecen esculturas artificiales.",
                "q1": "iridescent rainbow bismuth crystal geometric staircases",
                "q2": "metallic colorful kaleidoscope reflection geometry"
            }
        ]
    },

    # Video 44: Sonidos & Acústica del Planeta Vol 1
    {
        "id": "44_EnigmaIQ_5_Cosas_Vol24",
        "title": "5 Sonidos MISTERIOSOS de la Tierra que la ciencia investigó 🔊🌊",
        "headline_top": "5 SONIDOS MISTERIOSOS",
        "headline_bottom": "QUE LA CIENCIA INVESTIGÓ",
        "category": "ACÚSTICA & MISTERIOS",
        "description": "Sonidos inexplicables captados en el océano y templos antiguos 🔊 El monstruoso Bloop del Pacífico y las cámaras más silenciosas del planeta.\n\n#EnigmaIQ #Sonidos #Misterios #Oceano #Fisica #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. En mil novecientos noventa y siete, hidrófonos submarinos captaron en el Pacífico sur un sonido ultrasónico aterrador.",
                "p2": "Bautizado como The Bloop, se escuchó a cinco mil kilómetros de distancia; años después se confirmó que era la gigantesca fractura de un iceberg antártico.",
                "q1": "massive iceberg breaking falling ocean waves splash",
                "q2": "sonar acoustic audio waveform radar screen"
            },
            {
                "num": 2,
                "p1": "Número dos. El cambio de tono en la sirena de una ambulancia al acercarse y luego alejarse de ti no es que el chofer toque otro botón.",
                "p2": "Se llama Efecto Doppler y ocurre porque las ondas sonoras se comprimen al aproximarse a ti y se estiran en frecuencias más graves al distanciarse.",
                "q1": "emergency ambulance speeding lights flashing city street",
                "q2": "sound wave vibrations visual representation physics"
            },
            {
                "num": 3,
                "p1": "Número tres. La cámara anecoica de los laboratorios Orfield en Minnesota es considerada el lugar más silencioso de toda la faz de la Tierra.",
                "p2": "Absorbe el noventa y nueve coma nueve por ciento de los ecos; si estás más de media hora dentro comenzarás a oír tus propios órganos y la sangre en tu cabeza.",
                "q1": "anechoic sound proof chamber acoustic wedges foam",
                "q2": "person sitting quiet meditation dark room"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Al aplaudir frente a la pirámide de Kukulkán en Chichén Itzá, el eco que rebota en las escaleras te dejará helado.",
                "p2": "Los ingenieros mayas calcularon la separación y pendiente exacta de los peldaños para que el rebote del sonido imitara el canto sagrado del quetzal.",
                "q1": "chichen itza pyramid kukulkan sunny mexico",
                "q2": "colorful resplendent quetzal bird tropical rainforest"
            },
            {
                "num": 5,
                "p1": "Número cinco. El rugido de un tigre siberiano emite ondas de infrasonido inaudibles para el oído humano pero con efectos físicos reales.",
                "p2": "Estas frecuencias ultra bajas son capaces de atravesar bosques densos y tienen la propiedad biológica de paralizar momentáneamente a sus presas del susto.",
                "q1": "bengal tiger roaring aggressive mouth open teeth",
                "q2": "deep jungle fog wilderness trees wildlife"
            }
        ]
    },

    # Video 45: Medicina Antigua & Curas Bizarras Vol 1
    {
        "id": "45_EnigmaIQ_5_Cosas_Vol25",
        "title": "5 Tratamientos MÉDICOS del pasado que hoy parecen torturas 🩸💀",
        "headline_top": "5 TRATAMIENTOS MÉDICOS",
        "headline_bottom": "QUE HOY PARECEN TORTURAS",
        "category": "MEDICINA BIZARRA",
        "description": "Lo que los médicos del pasado recetaban te pondrá la piel de gallina 🩸 Trepanaciones, sangre de momia y jarabes infantiles de cocaína.\n\n#EnigmaIQ #Historia #Medicina #CurasAntiguas #Misterios #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. La trepanación craneal es uno de los procedimientos quirúrgicos más antiguos y sangrientos de la historia humana.",
                "p2": "Los médicos perforaban un agujero directo en el cráneo de los pacientes conscientes con piedras afiladas para liberar supuestos demonios o curar migrañas.",
                "q1": "ancient skull with surgical trepanation hole museum",
                "q2": "vintage medical surgical instruments historical metal"
            },
            {
                "num": 2,
                "p1": "Número dos. Aunque suene a práctica medieval, las sanguijuelas medicinales siguen utilizándose hoy en prestigiosos quirófanos modernos.",
                "p2": "En microcirugía reconstructiva ayudan a restablecer la circulación venosa al segregar hirudina, un potente anticoagulante natural que previene necrosis.",
                "q1": "medical leech close up clean water",
                "q2": "modern hospital surgery room doctors operating lights"
            },
            {
                "num": 3,
                "p1": "Número tres. El primer emperador de China, Qin Shi Huang, consumía regularmente perlas de mercurio líquido para intentar ser inmortal.",
                "p2": "Irónicamente, la toxicidad del metal pesado destruyó sus riñones, hígado y cordura mental provocándole la muerte por envenenamiento a los cuarenta y nueve años.",
                "q1": "liquid metal mercury droplets rolling shiny",
                "q2": "terracotta warriors ancient chinese emperor tomb"
            },
            {
                "num": 4,
                "p1": "Número cuatro. Durante los siglos dieciocho y diecinueve, miles de momias egipcias fueron desenterradas y molidas en polvo fino.",
                "p2": "Los médicos vendían ese polvo en boticas como remedio contra la peste y los artistas lo mezclaban como óleo para crear el pigmento marrón momia.",
                "q1": "egyptian golden mummy sarcophagus museum exhibit",
                "q2": "artist mixing oil paint brush palette canvas"
            },
            {
                "num": 5,
                "p1": "Número cinco. A finales del siglo diecinueve, potentes sustancias como la heroína y la cocaína se vendían libremente en jarabes infantiles.",
                "p2": "La farmacéutica Bayer comercializaba la heroína como jarabe calmante contra la tos para bebés asegurando que era una alternativa segura y no adictiva.",
                "q1": "vintage cough syrup medicine bottle 1800s retro label",
                "q2": "vintage apothecary old wooden medicine drawers"
            }
        ]
    },

    # Video 46: Lenguaje, Palabras & Expresiones Curiosas Vol 1
    {
        "id": "46_EnigmaIQ_5_Cosas_Vol26",
        "title": "5 Palabras que usas TODOS LOS DÍAS y no sabes de dónde vienen 🗣️💬",
        "headline_top": "5 PALABRAS QUE USAS A DIARIO",
        "headline_bottom": "Y SU SORPRENDENTE ORIGEN",
        "category": "ORIGEN DE PALABRAS",
        "description": "Las expresiones cotidianas esconden orígenes increíbles 🗣️ ¿De dónde viene la palabra OK, Ojalá o Salario? Descubre la historia del lenguaje.\n\n#EnigmaIQ #Lenguaje #Palabras #Historia #Etimologia #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. La conocida expresión española ojalá no tiene un origen latino ni europeo.",
                "p2": "Proviene directamente del árabe andalusí in sha Allah, que significa literalmente si Dios quiere, heredada tras ocho siglos de convivencia en la península.",
                "q1": "alhambra granada arabic palace sunny architecture",
                "q2": "ancient calligraphy writing manuscript parchment"
            },
            {
                "num": 2,
                "p1": "Número dos. La letra ñ, el símbolo más representativo del idioma español, nació por una necesidad de ahorrar espacio y tinta en manuscritos.",
                "p2": "Los monjes copistas medievales abreviaban la doble letra n colocando una pequeña virgulilla ondulada encima de una sola n para no gastar pergamino caro.",
                "q1": "medieval monk writing parchment quill feather ink",
                "q2": "antique leather book illuminated manuscript close up"
            },
            {
                "num": 3,
                "p1": "Número tres. La palabra universal OK es utilizada en casi todos los rincones del planeta pero nació como una broma satírica periodística.",
                "p2": "En mil ochocientos treinta y nueve, un diario de Boston la usó como una abreviatura humorística mal escrita de all correct deletreado con o y k.",
                "q1": "vintage 1800s newspaper printing press machine",
                "q2": "person thumbs up ok hand sign smiling sunny"
            },
            {
                "num": 4,
                "p1": "Número cuatro. El término económico salario que recibes mes a mes por tu trabajo proviene directamente de la sal común.",
                "p2": "En el antiguo imperio romano los soldados recibían una bolsa de sal marina llamada salarium para sazonar alimentos y conservar carne en sus campañas.",
                "q1": "stack of crisp paper money banknotes currency",
                "q2": "coarse sea salt crystals white piles culinary"
            },
            {
                "num": 5,
                "p1": "Número cinco. El alfabeto fonético internacional que usan pilotos y policías con palabras como Alfa, Bravo y Charlie fue creado por la OTAN.",
                "p2": "Se eligieron palabras universales que no pudieran confundirse ni distorsionarse por estática en frecuencias de radio con diferentes acentos mundiales.",
                "q1": "commercial airline cockpit pilot headset radio communications",
                "q2": "aircraft flying high altitude clouds sunny sky"
            }
        ]
    },

    # Video 47: Gigantes del Pasado & Megafauna Extinta Vol 1
    {
        "id": "47_EnigmaIQ_5_Cosas_Vol27",
        "title": "5 Monstruos REALES que dominaron la Tierra antes que nosotros 🦖🦴",
        "headline_top": "5 MONSTRUOS REALES QUE",
        "headline_bottom": "DOMINARON EL PLANETA",
        "category": "PALEONTOLOGÍA & MONSTRUOS",
        "description": "La Tierra estuvo poblada por colosos que parecen de pesadilla 🦖 Desde el Megalodón hasta la serpiente gigante Titanoboa.\n\n#EnigmaIQ #Dinosaurios #Megafauna #Fosiles #Historia #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. El colosal tiburón Megalodón fue el mayor depredador marino que jamás haya nadado en los mares de nuestro planeta.",
                "p2": "Llegaba a medir hasta dieciocho metros de longitud, el tamaño de un autobús articulado, y cada uno de sus dientes superaba el tamaño de una mano humana.",
                "q1": "megalodon shark swimming underwater prehistoric 3d",
                "q2": "fossilized megalodon shark tooth held in hand"
            },
            {
                "num": 2,
                "p1": "Número dos. La Titanoboa fue la serpiente más titánica y aterradora que jamás se arrastró por las selvas tropicales de Sudamérica.",
                "p2": "Con catorce metros de largo y más de mil kilos de peso, era tan colosal que cazaba y devoraba cocodrilos gigantes enteros de un solo bocado.",
                "q1": "giant python snake moving through tropical jungle",
                "q2": "crocodile swimming river tropical marsh swamp"
            },
            {
                "num": 3,
                "p1": "Número tres. El dinosaurio Argentinosaurus ostenta el récord indiscutible como el animal terrestre más pesado de la historia biológica.",
                "p2": "Con casi cuarenta metros de cabeza a cola y más de setenta toneladas, su peso colosal equivalía al de más de diez elefantes adultos juntos.",
                "q1": "giant sauropod dinosaur walking prehistoric landscape 3d",
                "q2": "herd of african elephants walking savanna dusty"
            },
            {
                "num": 4,
                "p1": "Número cuatro. El Megatherium o perezoso gigante terrestre habitó América y era una bestia del tamaño de un elefante moderno.",
                "p2": "A diferencia de los lentos perezosos de copa actuales, caminaba erguido sobre dos patas, pesaba cuatro toneladas y poseía garras de medio metro.",
                "q1": "prehistoric giant ground sloth skeleton museum exhibit",
                "q2": "cute modern sloth hanging upside down tree branch"
            },
            {
                "num": 5,
                "p1": "Número cinco. El temible tigre dientes de sable poseía dos colmillos superiores curvos de hasta veinte centímetros de longitud.",
                "p2": "Sin embargo, sus colmillos eran frágiles ante forcejeos, por lo que mordía con precisión quirúrgica el cuello de sus presas evitando golpear huesos duros.",
                "q1": "smilodon saber tooth cat roaring snow prehistoric 3d",
                "q2": "saber tooth tiger skull fangs museum fossil"
            }
        ]
    },

    # Video 48: Vida Microscópica & Monstruos Invisibles Vol 1
    {
        "id": "48_EnigmaIQ_5_Cosas_Vol28",
        "title": "5 Criaturas INVISIBLES que viven sobre tu cuerpo ahora mismo 🔬🪱",
        "headline_top": "5 CRIATURAS INVISIBLES",
        "headline_bottom": "QUE VIVEN EN TU CUERPO",
        "category": "MICROBIOLOGÍA & CUERPO",
        "description": "No estás solo: millones de seres microscópicos habitan en tu piel y pestañas 🔬 Descubre los ácaros faciales y las células asesinas de tu sangre.\n\n#EnigmaIQ #Microscopio #Bacterias #CuerpoHumano #Ciencia #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. Ahora mismo en las raíces de tus pestañas y poros de tu cara viven miles de diminutos ácaros transparentes llamados Demodex.",
                "p2": "Son seres microscópicos completamente inofensivos de ocho patas que salen de noche sobre tu piel para alimentarse de células muertas y sebo natural.",
                "q1": "human eyelashes eye close up macro skin",
                "q2": "microscopic demodex mite scanning electron microscope"
            },
            {
                "num": 2,
                "p1": "Número dos. Si contaras todas las células de tu cuerpo, descubrirías que tienes más bacterias que células humanas propias.",
                "p2": "Albergas casi cuarenta billones de microorganismos beneficiosos en tu piel e intestino, indispensables para digerir comida y defenderte de patógenos.",
                "q1": "gut bacteria microbiome flora 3d render colorful",
                "q2": "human hands washing clean soap water"
            },
            {
                "num": 3,
                "p1": "Número tres. Los bacteriófagos son virus naturales con una apariencia geométrica idéntica a una nave de aterrizaje espacial robótica.",
                "p2": "Inyectan su material genético exclusivamente dentro de bacterias dañinas para hacerlas estallar, salvando miles de vidas contra bacterias resistentes.",
                "q1": "bacteriophage virus attacking bacteria 3d science render",
                "q2": "laboratory genetic research microscope petri dish"
            },
            {
                "num": 4,
                "p1": "Número dos. Tu sistema inmunitario cuenta con un escuadrón de glóbulos blancos especializados llamados células asesinas naturales o Natural Killers.",
                "p2": "Patrullan tus venas día y noche detectando células infectadas por virus o células precancerosas para perforar su membrana e inducir su destrucción.",
                "q1": "white blood cell destroying cancer cell immune system 3d",
                "q2": "blood stream red blood cells flowing vein medical"
            },
            {
                "num": 5,
                "p1": "Número cinco. El polvo que se acumula sobre los muebles de tu habitación no proviene todo de la calle ni de la suciedad exterior.",
                "p2": "Casi un setenta por ciento del polvo doméstico está compuesto por millones de escamas microscópicas de piel humana muerta que desprendes a diario.",
                "q1": "dust particles floating in bright sunbeam room",
                "q2": "human skin epidermis layers anatomy 3d medical"
            }
        ]
    },

    # Video 49: El Océano Profundo & Zonas Fantasma Vol 3
    {
        "id": "49_EnigmaIQ_5_Cosas_Vol29",
        "title": "5 Anomalías del OCÉANO que los científicos NO pueden explicar 🌊🚢",
        "headline_top": "5 ANOMALÍAS DEL OCÉANO",
        "headline_bottom": "QUE LA CIENCIA INVESTIGA",
        "category": "ABISMOS & ANOMALÍAS",
        "description": "Las anomalías más misteriosas del fondo marino 🌊 Ríos bajo el agua, bosques gigantes sumergidos y chimeneas a 400 grados centígrados.\n\n#EnigmaIQ #Oceano #Misterios #Ciencia #Abismos #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. En la península de Yucatán existen cenotes que albergan auténticos ríos y lagos submarinos que fluyen bajo el agua salada.",
                "p2": "Una densa capa de sulfuro de hidrógeno separa el agua dulce superior del agua salada profunda creando una corriente con orillas y niebla bajo el mar.",
                "q1": "underwater cenote river diver swimming cave",
                "q2": "mexican cenote sunlight beam underwater emerald"
            },
            {
                "num": 2,
                "p1": "Número dos. En las costas del océano Pacífico crecen colosales bosques submarinos de algas gigantes kelp de más de treinta metros de altura.",
                "p2": "Crecen hasta sesenta centímetros diarios gracias a flotadores de gas naturales en sus hojas, creando un refugio vital para miles de especies marinas.",
                "q1": "giant kelp forest underwater sunlight diver swimming",
                "q2": "sea otter floating wrapped in green kelp"
            },
            {
                "num": 3,
                "p1": "Número tres. En las cordilleras volcánicas del fondo oceánico brotan chimeneas hidrotermales conocidas como fumaderas negras.",
                "p2": "Expulsan agua hirviendo cargada de minerales a más de cuatrocientos grados centígrados donde proliferan ecosistemas completos que jamás han visto la luz del Sol.",
                "q1": "deep sea hydrothermal black smoker vent mineral smoke",
                "q2": "giant tube worms underwater volcanic vent ecosystem"
            },
            {
                "num": 4,
                "p1": "Número cuatro. El misterio de las desapariciones en el Triángulo de las Bermudas tiene una explicación geológica en el fondo del mar.",
                "p2": "Enormes bolsas subterráneas de gas metano pueden liberarse de golpe en el agua reduciendo drásticamente la flotabilidad de los barcos hasta hundirlos.",
                "q1": "stormy rough ocean waves dark clouds shipwreck",
                "q2": "methane gas bubbles rising underwater sea"
            },
            {
                "num": 5,
                "p1": "Número cinco. En los mares del norte existen cascadas submarinas gigantescas con caídas mucho mayores que cualquier catarata de tierra firme.",
                "p2": "La catarata del Estrecho de Dinamarca precipita agua fría hiperdensa a más de tres mil metros de profundidad impulsando toda la circulación termohalina global.",
                "q1": "massive waterfall falling deep canyon aerial nature",
                "q2": "deep blue sea current satellite oceanography earth"
            }
        ]
    },

    # Video 50: Curiosidades del Futuro & Ciencia de Vanguardia Vol 1
    {
        "id": "50_EnigmaIQ_5_Cosas_Vol30",
        "title": "5 Tecnologías del FUTURO que ya son una REALIDAD 🤖⚡",
        "headline_top": "5 TECNOLOGÍAS DEL FUTURO",
        "headline_bottom": "QUE YA SON UNA REALIDAD",
        "category": "FUTURO & TECNOLOGÍA",
        "description": "La ciencia ficción ya está aquí 🤖 Computación cuántica, fusión nuclear limpia, órganos en impresoras 3D y el supermaterial grafeno.\n\n#EnigmaIQ #Futuro #Tecnologia #Ciencia #Innovacion #Curiosidades #XpressTV",
        "curiosities": [
            {
                "num": 1,
                "p1": "Número uno. Las computadoras cuánticas no procesan ceros y unos como tu teléfono o computador convencional.",
                "p2": "Utilizan qubits que gracias al principio de superposición cuántica pueden ser cero y uno simultáneamente, resolviendo en segundos cálculos que tardarían miles de años.",
                "q1": "quantum computer golden chandelier cryogenic lab",
                "q2": "digital abstract glowing qubits data processing"
            },
            {
                "num": 2,
                "p1": "Número dos. Los reactores de fusión nuclear como el ITER buscan recrear en la Tierra exactamente la misma fuente de energía que alimenta al Sol.",
                "p2": "Al fusionar isótopos de hidrógeno en campos magnéticos de plasma a ciento cincuenta millones de grados, generan energía limpia infinita sin residuos radiactivos.",
                "q1": "tokamak nuclear fusion reactor glowing purple plasma",
                "q2": "sun bright corona burning solar flares space"
            },
            {
                "num": 3,
                "p1": "Número tres. El telescopio espacial James Webb es tan potente que puede captar la luz de las primeras galaxias nacidas hace trece mil millones de años.",
                "p2": "Su enorme espejo dorado cubierto de oro puro y sus sensores infrarrojos congelados le permiten observar a través de nubes de polvo cósmico impenetrables.",
                "q1": "james webb space telescope gold mirrors space orbit",
                "q2": "deep field distant galaxies nebula cosmic star cluster"
            },
            {
                "num": 4,
                "p1": "Número cuatro. En laboratorios de bioingeniería avanzada ya se imprimen tejidos y órganos vivos utilizando impresoras tres D de alta precisión.",
                "p2": "En lugar de plástico usan biotintas celulares del propio paciente para imprimir diminutos corazones, cartílagos y córneas funcionales que evitan el rechazo inmune.",
                "q1": "3d bioprinter printing cellular tissue medical lab",
                "q2": "petri dish living stem cells growing biotechnology"
            },
            {
                "num": 5,
                "p1": "Número cinco. El grafeno es considerado el material milagroso más fuerte y conductor descubierto por la ciencia moderna.",
                "p2": "Tiene apenas un átomo de espesor, es doscientas veces más resistente que el acero templado, es más flexible que la goma y conduce electricidad mejor que el cobre.",
                "q1": "graphene honeycomb molecular lattice structure 3d render",
                "q2": "flexible transparent touchscreen glass technology"
            }
        ]
    }
]

def main():
    out_file = Path(r"C:\Users\Vanes\.gemini\antigravity\scratch\AI-Content-Automation-Engine1\flows\image_content_generator\pipeline\curiosities_30_catalog.json")
    
    # Check word counts and structure
    print(f"📊 Validating Catalog of {len(CATALOG)} Videos...")
    total_curiosities = 0
    all_curiosities_texts = set()
    
    for idx, v in enumerate(CATALOG, 1):
        c_list = v["curiosities"]
        assert len(c_list) == 5, f"Video {v['id']} does not have 5 curiosities (found {len(c_list)})"
        
        # Calculate narration length
        intro_words = 12
        outro_words = 16
        curiosity_words = sum(len(c["p1"].split()) + len(c["p2"].split()) for c in c_list)
        total_words = intro_words + outro_words + curiosity_words
        est_sec = total_words / 2.7  # XpressTV cadence
        
        for c in c_list:
            total_curiosities += 1
            full_c = c["p1"] + " " + c["p2"]
            c["text"] = full_c
            all_curiosities_texts.add(full_c)
            
        print(f"  [{idx:02d}/30] {v['id']}: ~{total_words} words -> ~{est_sec:.1f}s (>60s rule: {est_sec >= 60.0})")
        
    print(f"\n🎉 Total Unique Curiosities: {len(all_curiosities_texts)} / {total_curiosities}")
    assert len(all_curiosities_texts) == total_curiosities, "ERROR: Duplicate curiosities detected!"
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(CATALOG, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Catalog saved to {out_file.name} ({out_file.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    main()
