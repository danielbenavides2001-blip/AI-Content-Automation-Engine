import difflib
import re
import unicodedata
from typing import List, Set, Tuple, Optional
from tools.common.messenger import Messenger

class TopicValidator:
    """
    Robust Anti-Repetition and Topic Similarity Detection Engine.
    Prevents duplicate content across Facebook Feed Images, Reels, and Stories.
    """

    STOPWORDS: Set[str] = {
        "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "al", "a",
        "en", "por", "para", "con", "sin", "sobre", "entre", "que", "y", "o", "u", "e",
        "se", "su", "sus", "como", "mas", "menos", "muy", "tan", "este", "esta", "estos",
        "estas", "lo", "le", "les", "me", "te", "nos", "es", "son", "fue", "era", "ser",
        "primer", "primera", "primeros", "primeras", "mundo", "historia", "tierra", "planeta",
        "vida", "ano", "anos", "siglo", "siglos", "misterio", "misterios", "secreto", "secretos",
        "curiosidad", "curiosidades", "caso", "casos", "descubren", "descubrimiento", "revelan",
        "hallan", "increible", "asombroso", "imposible", "nuevo", "parte", "nivel", "niveles",
        "enigmas", "enigmaiq", "desafio", "desafia", "revelado", "oculto", "oculta"
    }

    GENERIC_WORDS: Set[str] = {
        "grande", "marino", "extremo", "antiguo", "humano", "origen", "fuerza", "cuerpo",
        "gigante", "profundo", "tiempo", "espacio", "fuego", "piedra", "tierra", "planeta",
        "estrella", "animal", "planta", "sistema", "sonido", "luz", "noche", "blanco",
        "negro", "rojo", "azul", "verde", "agua", "hielo", "viento", "montana", "valle",
        "cueva", "bosque", "selva", "isla", "rio", "lago", "mar", "criatura", "reino",
        "naturaleza", "universo", "galaxia", "solar", "oceanico", "submarino", "terrestre"
    }

    # Semantic clusters mapping known synonyms, aliases, and recurring entity variations
    ENTITY_CLUSTERS: List[Set[str]] = [
        {"tardigrado", "tardigrada", "oso de agua", "water bear"},
        {"darvaza", "puerta al infierno", "crater de gas", "derweze"},
        {"helio", "superfluidez", "superfluido", "liquido que desafia la gravedad"},
        {"llama eterna", "fuego eterno", "eternal flame", "llama bajo la cascada"},
        {"cascada submarina", "catarata submarina", "catarata de dinamarca", "salto de agua submarino"},
        {"gobekli", "gobekli tepe", "primer templo"},
        {"anticitera", "antikythera"},
        {"voynich", "manuscrito voynich"},
        {"dunkleosteus"},
        {"titanoboa"},
        {"megalodon", "megalodonte"},
        {"derinkuyu", "ciudad subterranea de turquia", "kaymakli"},
        {"saqqara", "pajaro de saqqara", "planeador de saqqara"},
        {"paraceratherium", "indricotherium", "baluchitherium"},
        {"naica", "cueva de los cristales", "cristales gigantes de naica"},
        {"ojo del sahara", "estructura de richat", "richat"},
        {"svalbard", "boveda de semillas", "boveda del fin del mundo"},
        {"cascada de sangre", "cascadas de sangre", "blood falls"},
        {"gran atractor", "atractor cosmico"},
        {"doble rendija", "experimento de young"},
        {"tornillo de arquimedes"},
        {"acero de damasco", "espada de damasco"},
        {"klerksdorp", "esferas de klerksdorp"},
        {"bateria de bagdad"},
        {"quimbaya", "aviones de quimbaya", "artefactos de quimbaya"},
        {"sacsayhuaman"},
        {"moeraki", "esferas de moeraki", "rocas de moeraki"},
        {"camaron pistola", "chasquido sonico", "alpheidae"},
        {"pajaros del terror", "aves del terror", "phorusrhacidae", "titanis"},
        {"ajolote", "axolotl", "axolote"},
        {"catatumbo", "relampago del catatumbo"},
        {"mano de gloria"},
        {"sudario de turin", "sabana santa"},
        {"lineas de nazca", "geoglifos de nazca"},
        {"isla de pascua", "moai", "moais", "rapa nui"},
        {"mecanismo de heras", "hero de alejandria", "eolipila"},
        {"antartida bajo el hielo", "lago vostok"},
        {"triangulo de las bermudas"},
        {"fosa de las marianas", "abismo challenger"},
        {"coloso de rodas"},
        {"faro de alejandria"},
        {"manuscrito rohonc"},
        {"disco de festo", "phaistos"},
        {"mapa de piri reis"},
        {"piedra del destino", "piedra de scone"},
        {"anomalocaris"},
        {"hallucigenia"},
        {"arthropleura"},
        {"helicoprion"},
        {"entelodonte", "cerdo del infierno", "entelodont"},
        {"smilodon", "dientes de sable"},
        {"calamar colosal", "calamar gigante", "architeuthis"},
        {"sifonoforo", "siphonophore"},
        {"hongo de miel", "armillaria ostoyae"},
        {"welwitschia", "welwitschia mirabilis"},
        {"rafflesia", "flor cadaver", "rafflesia arnoldii"},
        {"titano", "titan de saturno", "luna titan"},
        {"europa luna de jupiter", "oceano de europa"},
        {"55 cancri e", "planeta de diamante"},
        {"hd 189733b", "lluvia de cristal"}
    ]

    @classmethod
    def normalize(cls, text: str) -> str:
        """
        Normalizes a string by stripping diacritics, lowercase, removing punctuation,
        and stripping technical/series prefixes and suffixes.
        """
        if not text:
            return ""
        
        # 1. Unicode decomposition (remove accents)
        norm = unicodedata.normalize("NFKD", str(text).lower()).encode("ASCII", "ignore").decode("utf-8")
        
        # 2. Strip technical hooks and prefixes
        norm = re.sub(r"\[hook\s*[ab]\]", " ", norm)
        norm = re.sub(r"enigmaiq(\s*(geografia|7\s*niveles))?", " ", norm)
        norm = re.sub(r"los\s*7\s*niveles\s*de", " ", norm)
        norm = re.sub(r"curiosity\s*(reel|image)(\s*\([^\)]+\))?", " ", norm)
        norm = re.sub(r"parte\s*\d+", " ", norm)
        norm = re.sub(r"nivel\s*\d+", " ", norm)
        norm = re.sub(r"sabias\s*que", " ", norm)
        
        # 3. Clean symbols/punctuation
        norm = re.sub(r"[^a-z0-9\s]", " ", norm)
        return " ".join(norm.split())

    @classmethod
    def extract_keywords(cls, text: str) -> Set[str]:
        """
        Extracts significant entity keywords (length >= 4, not in stopwords).
        """
        norm = cls.normalize(text)
        return {w for w in norm.split() if len(w) >= 4 and w not in cls.STOPWORDS}

    @classmethod
    def get_matched_cluster(cls, text: str) -> Optional[Set[str]]:
        """
        Returns the semantic entity cluster if any alias matches the text.
        """
        norm = cls.normalize(text)
        for cluster in cls.ENTITY_CLUSTERS:
            for entity in cluster:
                norm_entity = cls.normalize(entity)
                if norm_entity and (norm_entity in norm or norm in norm_entity):
                    return cluster
        return None

    @classmethod
    def clean_past_titles(cls, raw_titles: List[str]) -> List[str]:
        """
        Deduplicates and cleans raw titles without filtering out 'unsafe' words,
        ensuring the full blacklist is preserved.
        """
        clean = []
        for t in raw_titles:
            t_str = str(t).strip()
            if not t_str:
                continue
            # Remove technical prefixes
            t_clean = re.sub(r"\[Hook\s*[AB]\]", "", t_str, flags=re.IGNORECASE).strip()
            t_clean = re.sub(r"^Curiosity\s*(Reel|Image)\s*(\([^\)]+\))?:?", "", t_clean, flags=re.IGNORECASE).strip()
            if t_clean and len(t_clean) >= 4 and t_clean.lower() != "curiosity image":
                clean.append(t_clean)
        return list(dict.fromkeys(clean))

    @classmethod
    def is_duplicate(
        cls,
        candidate: str,
        past_titles: List[str],
        headline: str = ""
    ) -> Tuple[bool, str, str]:
        """
        Verifies whether a candidate topic or headline matches any previously published topic.
        Returns:
            (is_duplicate: bool, matched_past_title: str, reason: str)
        """
        cand_norm = cls.normalize(candidate)
        if not cand_norm:
            return False, "", ""

        cand_kw = cls.extract_keywords(candidate)
        if headline:
            cand_kw.update(cls.extract_keywords(headline))

        cand_cluster = cls.get_matched_cluster(candidate) or (cls.get_matched_cluster(headline) if headline else None)

        for past in past_titles:
            past_norm = cls.normalize(past)
            if not past_norm or len(past_norm) < 4:
                continue

            # Layer 1: Exact normalized match
            if cand_norm == past_norm:
                return True, past, "Coincidencia exacta de título normalizado"

            # Layer 2: Direct substring containment for substantial phrases (> 8 chars)
            if (len(cand_norm) > 8 and cand_norm in past_norm) or (len(past_norm) > 8 and past_norm in cand_norm):
                return True, past, "Subcadena directa contenida en título previo"

            # Layer 3: Semantic Entity Cluster match
            past_cluster = cls.get_matched_cluster(past)
            if cand_cluster and past_cluster and cand_cluster == past_cluster:
                matching_sample = list(cand_cluster)[:2]
                return True, past, f"Misma entidad en cluster semántico ({matching_sample})"

            # Layer 4: Keyword Overlap (2 or more significant non-stopword keywords)
            past_kw = cls.extract_keywords(past)
            shared = cand_kw.intersection(past_kw)
            if len(shared) >= 2:
                return True, past, f"2 o más palabras clave compartidas: {shared}"

            # Layer 5: SequenceMatcher ratio
            sim = difflib.SequenceMatcher(None, cand_norm, past_norm).ratio()
            if sim >= 0.65:
                return True, past, f"Alta similitud de texto ({sim:.2f})"

        return False, "", ""
