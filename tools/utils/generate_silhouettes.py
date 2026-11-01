import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
GEO_JSON_PATH = BASE_DIR / "flows" / "image_content_generator" / "remotion" / "src" / "real_country_geodata.json"
OUT_TS_PATH = BASE_DIR / "flows" / "image_content_generator" / "remotion" / "src" / "country_silhouettes.ts"

with open(GEO_JSON_PATH, "r", encoding="utf-8") as f:
    d = json.load(f)

flag_colors = {
    'colombia': ['#fcd116', '#003893', '#ce1126'],
    'ecuador': ['#ffdd00', '#034ea2', '#ed1c24'],
    'mexico': ['#006847', '#ffffff', '#ce1126'],
    'usa': ['#b22234', '#ffffff', '#3c3b6e'],
    'brasil': ['#009739', '#fedd00', '#012169'],
    'peru': ['#d91023', '#ffffff', '#d91023'],
    'chile': ['#0039a6', '#ffffff', '#d52b1e'],
    'argentina': ['#74acdf', '#ffffff', '#f6b40e'],
    'venezuela': ['#fcd116', '#003893', '#cf142b'],
}

landmarks = {
    'colombia': {'name': 'SIERRA NEVADA', 'x': 340, 'y': 110, 'detail': '5.775 msnm'},
    'ecuador': {'name': 'VOLCÁN CHIMBORAZO', 'x': 330, 'y': 360, 'detail': '6.263 msnm (Punto más cercano al Sol)'},
    'mexico': {'name': 'ANILLO DE CENOTES', 'x': 590, 'y': 360, 'detail': 'Cráter Chicxulub (Yucatán)'},
    'usa': {'name': 'FALLA DE SAN ANDRÉS', 'x': 100, 'y': 310, 'detail': '1.200 km de Tensión Tectónica'},
    'brasil': {'name': 'ACUÍFERO RÍO HAMZA', 'x': 320, 'y': 240, 'detail': '4.000 m Bajo el Amazonas'},
    'peru': {'name': 'CAÑÓN DEL COLCA', 'x': 420, 'y': 510, 'detail': '3.270 m de Profundidad'},
    'chile': {'name': 'DESIERTO DE ATACAMA', 'x': 370, 'y': 230, 'detail': 'Lugar más Árido de la Tierra'},
    'argentina': {'name': 'GLACIAR PERITO MORENO', 'x': 270, 'y': 590, 'detail': '250 km² de Hielo Continental'},
    'venezuela': {'name': 'RELÁMPAGO DEL CATATUMBO', 'x': 190, 'y': 150, 'detail': '250 Rayos / km² al Año'}
}

ts = '''// ==============================================================================
// HIGH-PRECISION NATURAL EARTH VECTOR SILHOUETTES & REGIONAL LANDMARKS
// True geographic cartography with authentic peninsulas, coastlines, and borders
// ==============================================================================

export interface LandmarkData {
  name: string;
  x: number;
  y: number;
  detail: string;
}

export interface SilhouetteData {
  path: string;
  viewBox: string;
  name: string;
  capital: string;
  coordinates: string;
  primary: string;
  accent: string;
  iso: string;
  flagColors: string[];
  landmark: LandmarkData;
}
'''

for k, v in d.items():
    fc = flag_colors.get(k, ['#00f5ff', '#ffffff', '#38bdf8'])
    lm = landmarks.get(k, {'name': 'CAPITAL REGIONAL', 'x': 350, 'y': 350, 'detail': 'Centro Geográfico'})
    ts += f'''
export const {k.upper()}_SVG_PATH = "{v['path']}";
export const {k.upper()}_VIEWBOX = "{v['viewBox']}";
'''

ts += '''
const BASE_SILHOUETTES: Record<string, SilhouetteData> = {
'''

for k, v in d.items():
    fc = flag_colors.get(k, ['#00f5ff', '#ffffff', '#38bdf8'])
    lm = landmarks.get(k, {'name': 'CAPITAL REGIONAL', 'x': 350, 'y': 350, 'detail': 'Centro Geográfico'})
    ts += f'''  {k}: {{
    path: {k.upper()}_SVG_PATH,
    viewBox: {k.upper()}_VIEWBOX,
    name: "{v['name']}",
    capital: "{v['capital']}",
    coordinates: "{v['coords']}",
    primary: "{v['primary']}",
    accent: "{v['accent']}",
    iso: "{v['iso']}",
    flagColors: {json.dumps(fc)},
    landmark: {json.dumps(lm)}
  }},
'''

ts += '''};

export const COUNTRY_SILHOUETTES: Record<string, SilhouetteData> = {
  ...BASE_SILHOUETTES,
  "méxico": BASE_SILHOUETTES.mexico,
  "estados unidos": BASE_SILHOUETTES.usa,
  "estados_unidos": BASE_SILHOUETTES.usa,
  "eeuu": BASE_SILHOUETTES.usa,
  "ee.uu.": BASE_SILHOUETTES.usa,
  "united states": BASE_SILHOUETTES.usa,
  "brazil": BASE_SILHOUETTES.brasil,
  "perú": BASE_SILHOUETTES.peru,
};
'''

with open(OUT_TS_PATH, "w", encoding="utf-8") as out:
    out.write(ts)
print("Updated country_silhouettes.ts with authentic Natural Earth maps successfully!")
