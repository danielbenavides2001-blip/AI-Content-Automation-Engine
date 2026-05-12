import pandas as pd
from pathlib import Path
import shutil

csv_path = Path("flows/image_content_generator/out_short/ideas_tracking.csv")
ideas_dir = Path("flows/image_content_generator/out_short/ideas")

if csv_path.exists():
    df = pd.read_csv(csv_path)
    
    # We keep only UPLOADED ones or those that might be Stories (category='stories')
    # But since there are no stories yet, we just keep UPLOADED.
    
    pending_ids = df[df["state"] != "UPLOADED"]["id"].tolist()
    
    # Filter CSV
    df_clean = df[df["state"] == "UPLOADED"]
    df_clean.to_csv(csv_path, index=False)
    print(f"Cleaned CSV. Removed {len(pending_ids)} pending ideas.")
    
    # Delete folders
    for pid in pending_ids:
        # Search for folder with id
        for folder in ideas_dir.glob(f"*_{pid}"):
            if folder.is_dir():
                shutil.rmtree(folder)
                print(f"Deleted folder: {folder.name}")
else:
    print("CSV not found.")
