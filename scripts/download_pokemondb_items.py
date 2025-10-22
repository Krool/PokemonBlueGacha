"""
Download item icons from PokemonDB (higher quality than placeholders)
Based on https://pokemondb.net/item/all
"""
import os
import csv
import urllib.request
from pathlib import Path
import time

# Base URL for PokemonDB item sprites
BASE_URL = "https://img.pokemondb.net/sprites/items/"

# Mapping of item names to PokemonDB URLs (kebab-case)
ITEM_NAME_MAPPING = {
    # Pokéballs
    "Master Ball": "master-ball",
    "Ultra Ball": "ultra-ball",
    "Great Ball": "great-ball",
    "Poké Ball": "poke-ball",
    "Safari Ball": "safari-ball",
    
    # Evolution Stones
    "Moon Stone": "moon-stone",
    "Fire Stone": "fire-stone",
    "Thunder Stone": "thunder-stone",
    "Water Stone": "water-stone",
    "Leaf Stone": "leaf-stone",
    
    # Medicine
    "Antidote": "antidote",
    "Burn Heal": "burn-heal",
    "Ice Heal": "ice-heal",
    "Awakening": "awakening",
    "Parlyz Heal": "paralyze-heal",
    "Full Restore": "full-restore",
    "Max Potion": "max-potion",
    "Hyper Potion": "hyper-potion",
    "Super Potion": "super-potion",
    "Potion": "potion",
    "Full Heal": "full-heal",
    "Revive": "revive",
    "Max Revive": "max-revive",
    
    # Battle Items
    "X Accuracy": "x-accuracy",
    "X Attack": "x-attack",
    "X Defend": "x-defense",
    "X Speed": "x-speed",
    "X Special": "x-sp-atk",  # Gen 1 X Special became X Sp. Atk
    "Guard Spec.": "guard-spec",
    "Dire Hit": "dire-hit",
    
    # Vitamins
    "HP Up": "hp-up",
    "Protein": "protein",
    "Iron": "iron",
    "Carbos": "carbos",
    "Calcium": "calcium",
    "Rare Candy": "rare-candy",
    
    # Other Items
    "Escape Rope": "escape-rope",
    "Repel": "repel",
    "Super Repel": "super-repel",
    "Max Repel": "max-repel",
    "Nugget": "nugget",
    "Poké Doll": "poke-doll",
    "Fresh Water": "fresh-water",
    "Soda Pop": "soda-pop",
    "Lemonade": "lemonade",
    "Gold Teeth": "gold-teeth",
}

def download_item_icons():
    """Download item icons from PokemonDB"""
    # Create backup directory
    backup_dir = Path("src/Assets/Sprites/Items_backup")
    items_dir = Path("src/Assets/Sprites/Items")
    
    # Make sure items directory exists
    items_dir.mkdir(parents=True, exist_ok=True)
    
    # Read CSV to get all items
    csv_path = Path("src/data/items_gen1.csv")
    if not csv_path.exists():
        csv_path = Path("data/items_gen1.csv")
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        items = list(reader)
    
    print(f"Found {len(items)} items in CSV")
    print(f"Mapped {len(ITEM_NAME_MAPPING)} items to PokemonDB URLs")
    print(f"\nDownloading icons from PokemonDB...\n")
    
    downloaded = 0
    skipped = 0
    failed = []
    
    for item in items:
        name = item['Name']
        
        # Skip TMs (they use type icons)
        if name.startswith('TM'):
            skipped += 1
            continue
        
        # Check if we have a mapping for this item
        if name not in ITEM_NAME_MAPPING:
            print(f"  [WARN] No mapping for '{name}'")
            failed.append((name, "No URL mapping"))
            continue
        
        # Get the PokemonDB filename
        db_name = ITEM_NAME_MAPPING[name]
        url = BASE_URL + db_name + ".png"
        
        # Get the local filename from CSV
        icon_path = item['Icon']
        local_filename = Path(icon_path).name
        local_path = items_dir / local_filename
        
        # Create backup if file exists
        if local_path.exists() and not backup_dir.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)
            print(f"  [BACKUP] Creating backup directory...")
        
        if local_path.exists():
            backup_path = backup_dir / local_filename
            if not backup_path.exists():
                import shutil
                shutil.copy2(local_path, backup_path)
        
        # Download the icon
        try:
            print(f"  Downloading {name}... ", end='', flush=True)
            urllib.request.urlretrieve(url, local_path)
            print(f"OK")
            downloaded += 1
            time.sleep(0.1)  # Be nice to the server
        except Exception as e:
            print(f"FAILED ({e})")
            failed.append((name, str(e)))
    
    print(f"\n{'='*60}")
    print(f"[SUCCESS] Downloaded {downloaded} new icons from PokemonDB")
    print(f"[SKIP] Skipped {skipped} items (TMs)")
    
    if failed:
        print(f"\n[WARN] Failed to download {len(failed)} icons:")
        for name, error in failed:
            print(f"  - {name}: {error}")
    
    if backup_dir.exists():
        print(f"\n[BACKUP] Original icons backed up to: {backup_dir}")
    
    print(f"\n[SUCCESS] All downloaded icons saved to: {items_dir}")

def preview_mappings():
    """Show which items will be downloaded"""
    csv_path = Path("src/data/items_gen1.csv")
    if not csv_path.exists():
        csv_path = Path("data/items_gen1.csv")
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        items = list(reader)
    
    print("Items that will be downloaded from PokemonDB:\n")
    
    will_download = []
    no_mapping = []
    is_tm = []
    
    for item in items:
        name = item['Name']
        if name.startswith('TM'):
            is_tm.append(name)
        elif name in ITEM_NAME_MAPPING:
            will_download.append((name, ITEM_NAME_MAPPING[name]))
        else:
            no_mapping.append(name)
    
    print(f"[OK] Will download ({len(will_download)}):")
    for name, db_name in will_download:
        print(f"  - {name} -> {BASE_URL}{db_name}.png")
    
    print(f"\n[SKIP] TMs (using type icons) ({len(is_tm)}):")
    for name in is_tm:
        print(f"  - {name}")
    
    if no_mapping:
        print(f"\n[WARN] No URL mapping ({len(no_mapping)}):")
        for name in no_mapping:
            print(f"  - {name}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--preview':
        preview_mappings()
    else:
        response = input("This will download icons from PokemonDB and replace existing icons.\nOriginals will be backed up. Continue? (y/n): ")
        if response.lower() == 'y':
            download_item_icons()
        else:
            print("Cancelled.")

