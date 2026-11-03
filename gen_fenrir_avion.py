import sys
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getcwd())

from tools.audio_generation.gemini import GeminiAudioGenerator

audio_gen = GeminiAudioGenerator()

script_text = (
    "¿Cómo puede un avión caer ocho kilómetros en un solo minuto? "
    "Le pasó a este jet privado que llevaba nueve personas de Texas a las Bahamas. "
    "Volaba más alto que el Everest en medio de una tormenta. "
    "Afuera, hacía cuarenta y siete grados bajo cero y el avión empezó a cubrirse de hielo. "
    "Un ala vuela como tu mano por la ventana del carro. La inclinas y el aire la levanta, "
    "pero el hielo le cambia la forma y el aire ya no la levanta igual. "
    "Los pilotos pidieron subir más buscando aire tranquilo, pero el avión se fue en picada y el piloto gritó: ¡Mayday, Mayday! "
    "Bajó ocho kilómetros en poco más de un minuto. Más rápido que un fórmula uno a fondo, pero hacia el suelo. "
    "Cayó casi en vertical junto a una calle de Florida, a metros de unas casas y dejó un cráter. "
    "Murieron las nueve personas a bordo. En tierra no se reportaron heridos. "
    "¿Fue el hielo? Todavía no se sabe. "
    "La respuesta está en la caja negra, que guardó lo que pasó en ese minuto. "
    "Esto es EnigmaIQ."
)

out_wav = Path("scratch/fenrir_caida_avion.wav")
out_wav.parent.mkdir(parents=True, exist_ok=True)
audio_gen.text_to_speech(script_text, out_wav)

# Convert to mp3
import subprocess
out_mp3 = Path("scratch/fenrir_caida_avion.mp3")
cmd = ["ffmpeg", "-y", "-i", str(out_wav), "-c:a", "libmp3lame", "-b:a", "192k", str(out_mp3)]
subprocess.run(cmd, check=True)

# Probe duration
cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(out_mp3)]
res = subprocess.run(cmd_dur, check=True, capture_output=True, text=True)
dur = float(res.stdout.strip())
print(f"FENRIR AUDIO GENERATED: {dur:.2f} seconds")
