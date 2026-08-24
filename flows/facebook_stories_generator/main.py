import argparse
import sys
from flows.facebook_stories_generator.pipeline import FacebookStoryPipeline
from tools.common.messenger import Messenger


def main():
    parser = argparse.ArgumentParser(description="Facebook Native 9:16 Stories Generator & Publisher")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate story card locally without uploading to Facebook"
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Generate and publish native story directly to Facebook Page"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of stories to generate in this run (default: 1)"
    )
    
    args = parser.parse_args()
    
    if not args.dry_run and not args.publish:
        parser.print_help()
        sys.exit(1)
        
    try:
        pipeline = FacebookStoryPipeline()
        pipeline.run(publish=args.publish, count=args.count)
    except Exception as e:
        Messenger.error(f"💥 Facebook Story Execution Failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
