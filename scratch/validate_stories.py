import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from flows.image_content_generator.pipeline.pipeline import Pipeline
from flows.image_content_generator.pipeline.schemas import VideoOrientation
from tools.text_generation.gemini import GeminiTextGenerator
from tools.common.messenger import Messenger

def validate_step1():
    Messenger.info("🔍 VALIDATING STEP 1 (Story Generation)...")
    try:
        pipeline = Pipeline(
            out_base=Path("flows/image_content_generator/out_short"),
            resource_base=Path("flows/image_content_generator/resources"),
            orientation=VideoOrientation.SHORT
        )

        # Mock titles to avoid
        extra_avoid = "Test Topic 1, Test Topic 2"
        
        # We only want to test the generation logic
        # We'll use a real Gemini call but won't save files if possible, 
        # or we'll just check if the methods exist and can be called.
        
        Messenger.info("   Testing PromptManagerShorts.generate_full_story...")
        idea_data, script, category = pipeline.prompt_manager.generate_full_story(
            pipeline.text_gen, titles_to_avoid=[], extra_avoid=extra_avoid
        )
        
        Messenger.success(f"✅ Idea Generated: {idea_data.title}")
        Messenger.success(f"✅ Category: {category}")
        Messenger.success(f"✅ Scenes Count: {len(script.scenes)}")
        if script.intrigue_header:
            Messenger.success(f"✅ Intrigue Header: {script.intrigue_header}")
        else:
            Messenger.warning("⚠️ No Intrigue Header generated (Check prompt).")
            
        Messenger.success("✨ STEP 1 VALIDATION SUCCESSFUL!")
        return True
    except Exception as e:
        Messenger.error(f"❌ STEP 1 VALIDATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    validate_step1()
