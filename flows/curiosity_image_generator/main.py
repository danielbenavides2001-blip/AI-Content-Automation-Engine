import argparse
import sys
from flows.curiosity_image_generator.pipeline import CuriosityPipeline
from tools.common.messenger import Messenger

def main():
    parser = argparse.ArgumentParser(description="Curiosity Photo Post Generator for Facebook")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate text and image locally but do not upload to Facebook"
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Generate text and image, and upload to the Facebook Page"
    )
    
    args = parser.parse_args()
    
    if not args.dry_run and not args.publish:
        parser.print_help()
        sys.exit(1)
        
    try:
        pipeline = CuriosityPipeline()
        pipeline.run(publish=args.publish)
    except Exception as e:
        Messenger.error(f"💥 Pipeline Execution Failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
