#!/usr/bin/env python3
"""
Fix missing sprites for Farfetch'd and Mr. Mime
"""

import requests
from pathlib import Path

def fix_missing_sprites():
    images_dir = Path("Assets/Sprites/Pokemon")
    
    # Farfetch'd - use farfetchd (no apostrophe)
    farfetchd_urls = [
        "https://img.pokemondb.net/sprites/red-blue/normal/farfetchd.png",
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/red-blue/83.png"
    ]
    
    # Mr. Mime - use mr-mime
    mr_mime_urls = [
        "https://img.pokemondb.net/sprites/red-blue/normal/mr-mime.png",
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/red-blue/122.png"
    ]
    
    # Try Farfetch'd
    print("Downloading Farfetch'd...")
    for url in farfetchd_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(images_dir / "083_Farfetch'd.png", 'wb') as f:
                    f.write(response.content)
                print(f"✓ Farfetch'd downloaded from {url}")
                break
        except:
            continue
    
    # Try Mr. Mime
    print("Downloading Mr. Mime...")
    for url in mr_mime_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(images_dir / "122_Mr. Mime.png", 'wb') as f:
                    f.write(response.content)
                print(f"✓ Mr. Mime downloaded from {url}")
                break
        except:
            continue

if __name__ == "__main__":
    fix_missing_sprites()

