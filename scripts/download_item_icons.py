"""
Download item icons from PokéSprite repository
"""
import os
import csv
import urllib.request
from pathlib import Path

# Base URL for PokéSprite items
BASE_URL = "https://raw.githubusercontent.com/msikma/pokesprite/master/items/"

def download_item_icons():
    """Download all item icons from the CSV"""
    # Create items directory
    items_dir = Path("Assets/Sprites/Items")
    items_dir.mkdir(parents=True, exist_ok=True)
    
    # Read CSV
    with open('data/items_gen1.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        items = list(reader)
    
    print(f"Downloading {len(items)} item icons...")
    
    downloaded = 0
    failed = []
    
    for item in items:
        icon_path = item['Icon']
        name = item['Name']
        
        # Full URL
        url = BASE_URL + icon_path
        
        # Local path
        local_path = items_dir / Path(icon_path).name
        
        # Create subdirectory if needed
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Download if not exists
        if not local_path.exists():
            try:
                print(f"  Downloading {name}... ", end='')
                urllib.request.urlretrieve(url, local_path)
                print("✓")
                downloaded += 1
            except Exception as e:
                print(f"✗ ({e})")
                failed.append((name, icon_path, str(e)))
        else:
            print(f"  {name} already exists, skipping")
    
    print(f"\n✓ Downloaded {downloaded} new icons")
    
    if failed:
        print(f"\n⚠ Failed to download {len(failed)} icons:")
        for name, path, error in failed:
            print(f"  - {name} ({path}): {error}")
    
    print(f"\n✓ All item icons saved to {items_dir}")

if __name__ == "__main__":
    download_item_icons()

