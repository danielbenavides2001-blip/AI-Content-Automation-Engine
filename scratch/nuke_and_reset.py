import pandas as pd
from pathlib import Path
import shutil
import os

out_short = Path("flows/image_content_generator/out_short")
csv_path = out_short / "ideas_tracking.csv"
ideas_dir = out_short / "ideas"
history_json = out_short / "post_history.json"
last_type = Path(".last_post_type")

print("NUKING ALL DATA TO START FRESH...")

# 1. Reset CSV
if csv_path.exists():
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("id,title,state,category\n")
    print("Reset ideas_tracking.csv")

# 2. Delete all ideas
if ideas_dir.exists():
    for item in ideas_dir.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
    print("Deleted all idea folders")

# 3. Reset history
if history_json.exists():
    os.remove(history_json)
    print("Deleted post_history.json")

if last_type.exists():
    os.remove(last_type)
    print("Deleted .last_post_type")

print("SYSTEM IS NOW PURE. READY FOR STORIES-ONLY ERA.")
