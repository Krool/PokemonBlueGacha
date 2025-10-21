#!/usr/bin/env python3
"""
Download type icons from Bulbapedia Archives using correct URL pattern
"""

import requests
from pathlib import Path
import time

def download_type_icons():
    """Download type icons from Bulbapedia Archives"""
    
    icons_dir = Path("Assets/Sprites/Types")
    icons_dir.mkdir(parents=True, exist_ok=True)
    
    # Type icon URLs from Bulbapedia Archives (Sword/Shield style)
    type_urls = {
        'Normal': 'https://archives.bulbagarden.net/media/upload/9/95/Normal_icon_SwSh.png',
        'Fire': 'https://archives.bulbagarden.net/media/upload/a/ab/Fire_icon_SwSh.png',
        'Water': 'https://archives.bulbagarden.net/media/upload/8/80/Water_icon_SwSh.png',
        'Electric': 'https://archives.bulbagarden.net/media/upload/7/7b/Electric_icon_SwSh.png',
        'Grass': 'https://archives.bulbagarden.net/media/upload/a/a8/Grass_icon_SwSh.png',
        'Ice': 'https://archives.bulbagarden.net/media/upload/1/15/Ice_icon_SwSh.png',
        'Fighting': 'https://archives.bulbagarden.net/media/upload/3/3b/Fighting_icon_SwSh.png',
        'Poison': 'https://archives.bulbagarden.net/media/upload/8/8d/Poison_icon_SwSh.png',
        'Ground': 'https://archives.bulbagarden.net/media/upload/2/27/Ground_icon_SwSh.png',
        'Flying': 'https://archives.bulbagarden.net/media/upload/b/b5/Flying_icon_SwSh.png',
        'Psychic': 'https://archives.bulbagarden.net/media/upload/7/73/Psychic_icon_SwSh.png',
        'Bug': 'https://archives.bulbagarden.net/media/upload/9/9c/Bug_icon_SwSh.png',
        'Rock': 'https://archives.bulbagarden.net/media/upload/1/11/Rock_icon_SwSh.png',
        'Ghost': 'https://archives.bulbagarden.net/media/upload/0/01/Ghost_icon_SwSh.png',
        'Dragon': 'https://archives.bulbagarden.net/media/upload/7/70/Dragon_icon_SwSh.png',
    }
    
    print("Downloading type icons from Bulbapedia...\n")
    
    success_count = 0
    for type_name, url in type_urls.items():
        icon_path = icons_dir / f"{type_name}.png"
        
        if icon_path.exists():
            print(f"✓ {type_name}: Already exists")
            success_count += 1
            continue
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(icon_path, 'wb') as f:
                    f.write(response.content)
                print(f"✓ {type_name}: Downloaded")
                success_count += 1
            else:
                print(f"✗ {type_name}: Failed (Status: {response.status_code})")
        except Exception as e:
            print(f"✗ {type_name}: Error - {str(e)}")
        
        time.sleep(0.5)
    
    print(f"\n✓ Complete! {success_count}/{len(type_urls)} icons downloaded")
    print(f"Icons saved to: {icons_dir.absolute()}")

if __name__ == "__main__":
    download_type_icons()

