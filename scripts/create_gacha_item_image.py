"""
Create a placeholder gacha_item.png image
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_gacha_item_image():
    """Create a placeholder Items gacha machine image"""
    # Size similar to other gacha images
    width, height = 400, 500
    
    # Create image
    img = Image.new('RGB', (width, height), (40, 40, 60))  # Dark blue-gray background
    draw = ImageDraw.Draw(img)
    
    # Draw machine body (rounded rectangle)
    machine_rect = [50, 50, width-50, height-100]
    draw.rectangle(machine_rect, fill=(80, 80, 100), outline=(150, 150, 180), width=5)
    
    # Draw screen area
    screen_rect = [80, 80, width-80, 200]
    draw.rectangle(screen_rect, fill=(30, 30, 50), outline=(100, 100, 120), width=3)
    
    # Draw "ITEMS" text on screen
    try:
        font = ImageFont.truetype("arial.ttf", 60)
        small_font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageDraw.Font()
        small_font = ImageDraw.Font()
    
    # Title
    title = "ITEMS"
    bbox = draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    draw.text((text_x, 100), title, fill=(255, 215, 0), font=font)  # Gold text
    
    # Subtitle
    subtitle = "GACHA"
    bbox2 = draw.textbbox((0, 0), subtitle, font=small_font)
    text_width2 = bbox2[2] - bbox2[0]
    text_x2 = (width - text_width2) // 2
    draw.text((text_x2, 160), subtitle, fill=(200, 200, 220), font=small_font)
    
    # Draw item slots/circles (representing different items)
    slot_y = 250
    slot_spacing = 70
    slot_size = 50
    
    colors = [
        (255, 200, 200),  # Red - Balls
        (200, 200, 255),  # Blue - Stones
        (255, 255, 200),  # Yellow - Vitamins
        (200, 255, 200),  # Green - Medicine
        (255, 200, 255),  # Purple - TMs
    ]
    
    for i, color in enumerate(colors):
        x = 80 + (i * slot_spacing)
        draw.ellipse([x, slot_y, x+slot_size, slot_y+slot_size], 
                    fill=color, outline=(100, 100, 100), width=2)
    
    # Draw dispensing chute
    chute_rect = [width//2 - 60, height-80, width//2 + 60, height-40]
    draw.rectangle(chute_rect, fill=(50, 50, 70), outline=(120, 120, 140), width=3)
    
    # Draw slot/opening
    slot_rect = [width//2 - 40, height-75, width//2 + 40, height-65]
    draw.rectangle(slot_rect, fill=(20, 20, 30))
    
    # Save image
    output_path = Path("Assets/Sprites/Main/gacha_item.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    
    print(f"✓ Created {output_path}")
    print(f"  Size: {width}x{height}")
    print(f"  This is a placeholder - replace with a proper image for better visuals")

if __name__ == "__main__":
    create_gacha_item_image()

