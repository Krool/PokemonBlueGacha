"""
Fix item icon paths and create simple placeholder icons for missing items
"""
import csv
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Updated icon mapping with correct PokéSprite paths
corrected_paths = {
    "Moon Stone": "evo-stone/moon-stone.png",
    "Fire Stone": "evo-stone/fire-stone.png",
    "Thunder Stone": "evo-stone/thunder-stone.png",
    "Water Stone": "evo-stone/water-stone.png",
    "Leaf Stone": "evo-stone/leaf-stone.png",
    
    "Escape Rope": "hold-item/escape-rope.png",
    "Repel": "hold-item/repel.png",
    "Super Repel": "hold-item/super-repel.png",
    "Max Repel": "hold-item/max-repel.png",
    
    "HP Up": "hold-item/hp-up.png",
    "Protein": "hold-item/protein.png",
    "Iron": "hold-item/iron.png",
    "Carbos": "hold-item/carbos.png",
    "Calcium": "hold-item/calcium.png",
    "Rare Candy": "hold-item/rare-candy.png",
    
    "X Accuracy": "hold-item/x-accuracy.png",
    "X Attack": "hold-item/x-attack.png",
    "X Defend": "hold-item/x-defense.png",
    "X Speed": "hold-item/x-speed.png",
    "X Special": "hold-item/x-special.png",
    "Guard Spec.": "hold-item/guard-spec.png",
    "Dire Hit": "hold-item/dire-hit.png",
    
    "Nugget": "hold-item/nugget.png",
    "Poké Doll": "hold-item/poke-doll.png",
    "Fresh Water": "hold-item/fresh-water.png",
    "Soda Pop": "hold-item/soda-pop.png",
    "Lemonade": "hold-item/lemonade.png",
    "Coin": "other/coin.png",
    "Gold Teeth": "hold-item/gold-teeth.png",
}

def create_placeholder_icon(name, output_path, bg_color=(200, 200, 200)):
    """Create a simple placeholder icon"""
    # Create 32x32 image
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw rounded rectangle background
    draw.rectangle([2, 2, 30, 30], fill=bg_color, outline=(100, 100, 100), width=2)
    
    # Draw text (first 2-3 letters)
    text = name[:3].upper()
    try:
        # Try to use a small font
        font = ImageFont.truetype("arial.ttf", 10)
    except:
        font = ImageFont.load_default()
    
    # Get text size and center it
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (32 - text_width) // 2
    y = (32 - text_height) // 2
    
    draw.text((x, y), text, fill=(50, 50, 50), font=font)
    
    img.save(output_path)

def update_csv_and_create_placeholders():
    """Update CSV with corrected paths and create placeholders"""
    # Read existing CSV
    with open('data/items_gen1.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        items = list(reader)
    
    # Update paths
    for item in items:
        name = item['Name']
        if name in corrected_paths:
            item['Icon'] = corrected_paths[name]
    
    # Write updated CSV
    with open('data/items_gen1.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=items[0].keys())
        writer.writeheader()
        writer.writerows(items)
    
    print("✓ Updated CSV with corrected icon paths")
    
    # Create placeholder icons for items
    items_dir = Path("Assets/Sprites/Items")
    items_dir.mkdir(parents=True, exist_ok=True)
    
    # Category colors
    category_colors = {
        'ball': (200, 100, 100),
        'evo-stone': (150, 150, 200),
        'medicine': (100, 200, 100),
        'battle': (200, 150, 100),
        'vitamin': (200, 200, 100),
        'tm': (150, 100, 200),
        'valuable': (255, 215, 0),
        'other': (180, 180, 180),
    }
    
    created = 0
    for item in items:
        name = item['Name']
        category = item['Category']
        icon_file = Path(item['Icon']).name
        local_path = items_dir / icon_file
        
        # Create placeholder if doesn't exist
        if not local_path.exists():
            bg_color = category_colors.get(category, (200, 200, 200))
            create_placeholder_icon(name, local_path, bg_color)
            print(f"  Created placeholder for {name}")
            created += 1
    
    print(f"\n✓ Created {created} placeholder icons")
    print(f"✓ All item icons ready in {items_dir}")

if __name__ == "__main__":
    update_csv_and_create_placeholders()

