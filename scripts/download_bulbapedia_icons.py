"""
Download item icons from Bulbapedia for items missing from PokéSprite
"""
import urllib.request
import urllib.error
from pathlib import Path
import time

# Items that need icons from Bulbapedia
# Format: (item_name, bulbapedia_filename)
bulbapedia_items = [
    # Evolution Stones
    ("Moon Stone", "Dream_Moon_Stone_Sprite.png"),
    ("Fire Stone", "Dream_Fire_Stone_Sprite.png"),
    ("Thunder Stone", "Dream_Thunder_Stone_Sprite.png"),
    ("Water Stone", "Dream_Water_Stone_Sprite.png"),
    ("Leaf Stone", "Dream_Leaf_Stone_Sprite.png"),
    
    # Vitamins
    ("HP Up", "Dream_HP_Up_Sprite.png"),
    ("Protein", "Dream_Protein_Sprite.png"),
    ("Iron", "Dream_Iron_Sprite.png"),
    ("Carbos", "Dream_Carbos_Sprite.png"),
    ("Calcium", "Dream_Calcium_Sprite.png"),
    ("Rare Candy", "Dream_Rare_Candy_Sprite.png"),
    
    # Battle Items
    ("X Accuracy", "Dream_X_Accuracy_Sprite.png"),
    ("X Attack", "Dream_X_Attack_Sprite.png"),
    ("X Defend", "Dream_X_Defense_Sprite.png"),
    ("X Speed", "Dream_X_Speed_Sprite.png"),
    ("X Special", "Dream_X_Sp._Atk_Sprite.png"),
    ("Guard Spec.", "Dream_Guard_Spec._Sprite.png"),
    ("Dire Hit", "Dream_Dire_Hit_Sprite.png"),
    
    # Repels
    ("Repel", "Dream_Repel_Sprite.png"),
    ("Super Repel", "Dream_Super_Repel_Sprite.png"),
    ("Max Repel", "Dream_Max_Repel_Sprite.png"),
    
    # Other
    ("Escape Rope", "Dream_Escape_Rope_Sprite.png"),
    ("Nugget", "Dream_Nugget_Sprite.png"),
    ("Poké Doll", "Dream_Poke_Doll_Sprite.png"),
    ("Fresh Water", "Dream_Fresh_Water_Sprite.png"),
    ("Soda Pop", "Dream_Soda_Pop_Sprite.png"),
    ("Lemonade", "Dream_Lemonade_Sprite.png"),
    ("Coin", "Dream_Coin_Sprite.png"),
    ("Gold Teeth", "Dream_Gold_Teeth_Sprite.png"),
]

# Bulbapedia image base URL
BASE_URL = "https://archives.bulbagarden.net/media/upload/"

def get_bulbapedia_url(filename):
    """
    Generate Bulbapedia Archives URL for an image
    Format: https://archives.bulbagarden.net/media/upload/X/YZ/Filename.png
    where X is first char and YZ are first two chars of MD5 hash
    """
    # For simplicity, try common paths
    # Bulbapedia uses MD5 hashing for paths, but we can try direct paths
    return f"https://archives.bulbagarden.net/wiki/File:{filename}"

def download_from_bulbapedia():
    """Download icons from Bulbapedia"""
    items_dir = Path("Assets/Sprites/Items")
    items_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Attempting to download {len(bulbapedia_items)} icons from Bulbapedia...")
    print("Note: This will try to get the direct image URLs\n")
    
    downloaded = 0
    failed = []
    
    for item_name, bulba_filename in bulbapedia_items:
        local_filename = bulba_filename.replace("Dream_", "").replace("_Sprite", "").replace(" ", "_").lower()
        local_path = items_dir / local_filename
        
        # Skip if already exists and is not a placeholder
        if local_path.exists() and local_path.stat().st_size > 5000:  # Real images are bigger
            print(f"  {item_name} already exists with good size, skipping")
            continue
        
        # Try multiple URL patterns
        url_patterns = [
            f"https://raw.githubusercontent.com/msikma/pokesprite/master/items-outline/{local_filename}",
            f"https://raw.githubusercontent.com/msikma/pokesprite/master/items/{local_filename}",
            f"https://archives.bulbagarden.net/media/upload/{bulba_filename}",
        ]
        
        success = False
        for url in url_patterns:
            try:
                print(f"  Trying {item_name} from {url.split('/')[-2]}... ", end='')
                urllib.request.urlretrieve(url, local_path)
                
                # Check if it's a real image
                if local_path.stat().st_size > 1000:
                    print("✓")
                    downloaded += 1
                    success = True
                    time.sleep(0.5)  # Be nice to servers
                    break
                else:
                    print("✗ (too small)")
            except urllib.error.HTTPError as e:
                print(f"✗ (404)")
            except Exception as e:
                print(f"✗ ({e})")
        
        if not success:
            failed.append(item_name)
    
    print(f"\n✓ Downloaded {downloaded} new icons")
    
    if failed:
        print(f"\n⚠ Could not download {len(failed)} icons (will use placeholders):")
        for name in failed:
            print(f"  - {name}")
    
    print(f"\n✓ Icons ready in {items_dir}")

if __name__ == "__main__":
    download_from_bulbapedia()

