import os
import sys
import subprocess
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure environment variables are loaded
load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[3]
REMOTION_DIR = BASE_DIR / "flows" / "image_content_generator" / "remotion"
HISTORY_FILE = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "automated_posts_history.csv"

MASTER_CATALOG = {
    "ElPorqueDeTodoSierraNevada": {
        "title": "De la playa tropical a la nieve en 42 km: La montaña más insólita del planeta 🏔️🌊",
        "description": """¿Te imaginas salir de una playa del Caribe a 30°C y en la distancia de un maratón estar pisando glaciares de nieve eterna a más de 5.700 metros de altura?

Conoce la Sierra Nevada de Santa Marta (Colombia): una pirámide de roca que no pertenece a los Andes y cuyas rocas viajaron más de 2.100 kilómetros desde el Perú.

👉 Síguenos en @EnigmaIQ para conocer los récords y secretos más extremos de la Tierra.

#sierranevada #geologia #montaña #colombia #caribe #ciencia #curiosidades #enigmaiq #tierrasecreta #datoscuriosos #reels""",
        "tags": ["colombia", "geografia", "montañas", "curiosidades"]
    },
    "ElPorqueDeTodoAmazonas": {
        "title": "¿Por qué no hay ni un solo puente en 6.400 km de Río Amazonas? 🌊🚫🌉",
        "description": """El río Amazonas es el más caudaloso del planeta y cruza miles de kilómetros de territorio habitado... pero de punta a punta, no existe ni un solo puente que lo cruce. ¿Por qué la ingeniería moderna jamás ha construido uno?

1. En época de lluvias, el río sube hasta 15 metros y su ancho pasa de 5 km a más de 40 kilómetros de selva inundada.
2. El fondo no tiene roca firme: son decenas de metros de lodo blando e inestable.
3. No hay carreteras que unir: las comunidades viven del transporte fluvial.

👉 Síguenos en @EnigmaIQ para descubrir las respuestas a las preguntas más asombrosas del planeta.

#amazonas #rioamazonas #geografia #ingenieria #ciencia #curiosidades #enigmaiq #sabiasque #datoscuriosos #naturaleza #shorts #reels""",
        "tags": ["amazonas", "geografia", "ingenieria"]
    },
    "ElPorqueDeTodoOrquideas": {
        "title": "¿Por qué Colombia tiene más orquídeas que ningún otro país del planeta? 🌸🌿",
        "description": """Más de cuatro mil doscientas especies de orquídeas habitan en un solo país: Colombia supera a todo el planeta en variedad botánica. ¿Cuál es el secreto geográfico detrás de esta explosión floral?

La respuesta está en la división única de sus tres cordilleras andinas, creando miles de microclimas aislados con nubes perpetuas.

👉 Síguenos en @EnigmaIQ para desentrañar la ciencia de la naturaleza.

#orquideas #colombia #biodiversidad #botanica #andes #naturaleza #enigmaiq #curiosidades #flores #reels""",
        "tags": ["colombia", "botanica", "biodiversidad"]
    },
    "ElPorqueDeTodoCatatumbo": {
        "title": "El lugar con más relámpagos de la Tierra: La tormenta que nunca se apaga ⚡⛈️",
        "description": """Hasta 250 rayos por kilómetro cuadrado al año y tormentas que duran hasta 10 horas continuas durante 300 noches. 

El Relámpago del Catatumbo es el mayor generador natural de ozono del planeta y un enigma de la física meteorológica entre la Cordillera Oriental y el Lago de Maracaibo.

👉 Síguenos en @EnigmaIQ para desentrañar los mayores fenómenos de la Tierra.

#catatumbo #relampago #tormenta #meteorologia #colombia #venezuela #ciencia #naturaleza #curiosidades #enigmaiq #rayos #shorts #reels""",
        "tags": ["catatumbo", "meteorologia", "rayos"]
    },
    "ElPorqueDeTodoAjolote": {
        "title": "El misterio biológico del Ajolote: El animal que regenera su propio cerebro 🧬🦎",
        "description": """El ajolote no solo regenera sus extremidades: puede regenerar partes de su corazón, su columna vertebral y hasta su propio tejido cerebral sin dejar una sola cicatriz.

¿Cómo logra este anfibio desafiar las leyes del envejecimiento y la biología humana?

👉 Síguenos en @EnigmaIQ para conocer los secretos de la evolución.

#ajolote #biologia #regeneracion #ciencia #mexico #curiosidades #enigmaiq #genetica #naturaleza #reels""",
        "tags": ["ajolote", "biologia", "genetica"]
    },
    "ElPorqueDeTodoMedusa": {
        "title": "La medusa biológicamente inmortal que desafía a la muerte 🪼✨",
        "description": """Cuando la Turritopsis dohrnii envejece o sufre una herida grave, no muere. Realiza transdiferenciación celular, revirtiendo su ciclo de vida para volver a ser un pólipo joven.

Científicamente es el único organismo multicelular biológicamente inmortal de la Tierra.

👉 Síguenos en @EnigmaIQ para descubrir los mayores misterios de la ciencia.

#medusa #inmortalidad #biologia #oceano #ciencia #naturaleza #curiosidades #enigmaiq #sabiasque #shorts #reels""",
        "tags": ["medusa", "oceano", "inmortalidad"]
    }
}

def get_next_composition():
    # Read history to see which ones were posted
    posted_topics = set()
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) >= 3:
                        posted_topics.add(parts[2].strip().lower())
        except Exception:
            pass
            
    # Find first composition not recently posted
    for comp_id, meta in MASTER_CATALOG.items():
        if comp_id.lower() not in posted_topics and meta["title"].lower() not in posted_topics:
            return comp_id
            
    # Default fallback: Sierra Nevada (Colombia curiosity)
    return "ElPorqueDeTodoSierraNevada"

def render_master_video(composition_id: str, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"🎬 [Remotion] Renderizando composición maestra: '{composition_id}'...")
    print(f"   Destino: {out_path}")
    
    cmd = [
        "npx", "remotion", "render",
        "src/index.ts",
        composition_id,
        str(out_path),
        "--concurrency=4"
    ]
    # On Windows run with shell=True for npx
    is_win = sys.platform.startswith("win")
    subprocess.run(cmd, cwd=str(REMOTION_DIR), check=True, shell=is_win)
    
    if not out_path.exists() or out_path.stat().st_size < 100000:
        raise RuntimeError(f"El renderizado de Remotion falló o generó un archivo corrupto: {out_path}")
    print(f"✅ Render completado con éxito: {out_path.stat().st_size / (1024*1024):.2f} MB")

def publish_reel_to_facebook(video_path: Path, title: str, description: str, page_id: str, access_token: str):
    file_size = video_path.stat().st_size
    api_version = "v19.0"
    base_url = f"https://graph.facebook.com/{api_version}"
    
    print("\n📤 [Facebook Reel Publisher] Iniciando subida a Meta Graph API...")
    print(f"   Página ID: {page_id}")
    print(f"   Video: {video_path.name} ({file_size / (1024*1024):.2f} MB)")
    print(f"   Título: {title}")
    
    # 1. Start Phase
    start_res = requests.post(
        f"{base_url}/{page_id}/video_reels",
        json={"upload_phase": "start", "access_token": access_token}
    )
    start_res.raise_for_status()
    start_data = start_res.json()
    video_id = start_data["video_id"]
    upload_url = start_data["upload_url"]
    print(f"✅ [Meta API] Sesión de Reel iniciada (Video ID: {video_id})")
    
    # 2. Transfer Phase
    headers = {
        "Authorization": f"OAuth {access_token}",
        "offset": "0",
        "file_size": str(file_size)
    }
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    upload_res = requests.post(upload_url, headers=headers, data=video_bytes)
    upload_res.raise_for_status()
    print("✅ [Meta API] Binario de video transferido con éxito.")
    
    # 3. Finish Phase (Publish immediately)
    finish_payload = {
        "upload_phase": "finish",
        "access_token": access_token,
        "video_id": video_id,
        "video_state": "PUBLISHED",
        "description": description,
        "title": title
    }
    finish_res = requests.post(f"{base_url}/{page_id}/video_reels", json=finish_payload)
    if finish_res.status_code != 200:
        print(f"⚠️ Error al finalizar Reel: {finish_res.status_code} - {finish_res.text}")
        finish_res.raise_for_status()
        
    result = finish_res.json()
    print(f"🎉 [Facebook Reel Publisher] ¡Publicado con éxito en EnigmaIQ! {result}")
    return result

def main():
    parser = argparse.ArgumentParser(description="EnigmaIQ Master Remotion Publisher")
    parser.add_argument("--composition", type=str, default="", help="Composition ID to render")
    args = parser.parse_args()
    
    comp_id = args.composition.strip() if args.composition else get_next_composition()
    if comp_id not in MASTER_CATALOG:
        print(f"Composición '{comp_id}' no encontrada en el catálogo. Usando Sierra Nevada.")
        comp_id = "ElPorqueDeTodoSierraNevada"
        
    meta = MASTER_CATALOG[comp_id]
    print(f"\n========================================================")
    print(f"🚀 ENIGMAIQ MASTER REMOTION PIPELINE")
    print(f"🎬 Composición: {comp_id}")
    print(f"📌 Título: {meta['title']}")
    print(f"========================================================\n")
    
    out_video = BASE_DIR / "flows" / "image_content_generator" / "out_short" / f"{comp_id}_Master.mp4"
    render_master_video(comp_id, out_video)
    
    page_id = os.getenv("FACEBOOK_PAGE_ID", "976163608905137")
    access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
    
    if not access_token:
        print("⚠️ Advertencia: No se encontró FACEBOOK_PAGE_ACCESS_TOKEN. Saltando subida a Facebook.")
        sys.exit(0)
        
    publish_reel_to_facebook(out_video, meta["title"], meta["description"], page_id, access_token)
    
    # Log to history
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    import datetime
    today = datetime.date.today().isoformat()
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{today},video,{comp_id}\n")
    print(f"✅ Historial actualizado con '{comp_id}'.")

if __name__ == "__main__":
    main()
