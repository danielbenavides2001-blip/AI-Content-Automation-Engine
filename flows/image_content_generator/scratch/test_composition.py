import sys
from pathlib import Path
from PIL import Image, ImageDraw

# Reconfigure stdout/stderr to utf-8 to handle any unicode/emojis safely
if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add repository root to python path
sys.path.append(str(Path(__file__).resolve().parents[3]))

from flows.image_content_generator.pipeline.pipeline import Pipeline
from flows.image_content_generator.pipeline.schemas import VideoOrientation

def main():
    Messenger_info = print
    Messenger_info("Starting local composition test...")

    # Define paths
    scratch_dir = Path(__file__).parent
    scratch_dir.mkdir(parents=True, exist_ok=True)
    
    dummy_input = scratch_dir / "dummy_scene_01.png"
    dummy_output = scratch_dir / "test_composed_output.jpg"

    # 1. Create a beautiful dummy input image (9:16 aspect ratio, e.g., 1080x1920)
    Messenger_info("Creating beautiful dummy 9:16 base image...")
    img = Image.new("RGB", (1080, 1920), color=(30, 41, 59))
    draw = ImageDraw.Draw(img)
    
    # Draw simple elegant decorative gradient / shapes
    for y in range(1920):
        r = int(30 + (15 - 30) * y / 1920)
        g = int(41 + (23 - 41) * y / 1920)
        b = int(59 + (42 - 59) * y / 1920)
        draw.line([(0, y), (1080, y)], fill=(r, g, b))
        
    draw.ellipse([340, 760, 740, 1160], fill=(255, 223, 0), outline=(255, 255, 255), width=8)
    draw.ellipse([440, 860, 640, 1060], fill=(239, 68, 68))
    img.save(dummy_input)
    Messenger_info(f"Dummy base saved at {dummy_input}")

    # 2. Instantiate pipeline
    pipeline = Pipeline(
        out_base=Path("flows/image_content_generator/out_short"),
        resource_base=Path("flows/image_content_generator/resource"),
        orientation=VideoOrientation.SHORT
    )

    # 3. Test composition
    test_text = (
        "Los pulpos tienen tres corazones, nueve cerebros y su sangre es de color azul brillante "
        "debido a una proteína basada en cobre llamada hemocianina, que les ayuda a sobrevivir en "
        "las profundidades más frías del océano."
    )
    
    Messenger_info("Executing compose_sabias_que_card...")
    pipeline.compose_sabias_que_card(dummy_input, dummy_output, test_text)
    
    Messenger_info(f"Composition complete! Composed file saved at: {dummy_output}")

if __name__ == "__main__":
    main()
