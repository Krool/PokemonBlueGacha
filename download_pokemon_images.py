#!/usr/bin/env python3
"""
Download Pokémon images from Bulbapedia for Gen 1 Pokémon
Updates pokemon_gen1.csv with image filenames
"""

import csv
import requests
from pathlib import Path
import time
from urllib.parse import urljoin
import re

def download_pokemon_sprites():
    """Download sprites for all Gen 1 Pokémon"""
    
    # Create images directory
    images_dir = Path("Assets/Sprites/Pokemon")
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # Read the pokemon CSV
    pokemon_list = []
    with open('pokemon_gen1.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pokemon_list.append(row)
    
    print(f"Found {len(pokemon_list)} Pokémon to download\n")
    
    # Download images for each Pokémon
    for pokemon in pokemon_list:
        number = pokemon['Number']
        name = pokemon['Name']
        
        # Generate image filename
        image_filename = f"{number}_{name}.png"
        image_path = images_dir / image_filename
        
        # Skip if already exists
        if image_path.exists():
            print(f"✓ {name}: Already exists")
            pokemon['Image'] = f"Sprites/Pokemon/{image_filename}"
            continue
        
        # Try to download from Bulbapedia
        # The standard URL pattern for Gen 1 sprites on Bulbapedia
        sprite_url = f"https://archives.bulbagarden.net/media/upload/archive/a/a5/20160131101556%21Spr_1b_{number.lstrip('0')}.png"
        
        # Alternative: Try the current version
        alt_url = f"https://img.pokemondb.net/sprites/red-blue/normal/{name.lower().replace(' ', '-').replace('♀', '-f').replace('♂', '-m')}.png"
        
        try:
            # Try main URL first
            response = requests.get(sprite_url, timeout=10)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                print(f"✓ {name}: Downloaded from Bulbapedia")
                pokemon['Image'] = f"Sprites/Pokemon/{image_filename}"
            else:
                # Try alternative URL
                response = requests.get(alt_url, timeout=10)
                if response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    print(f"✓ {name}: Downloaded from PokemonDB")
                    pokemon['Image'] = f"Sprites/Pokemon/{image_filename}"
                else:
                    print(f"✗ {name}: Failed to download (Status: {response.status_code})")
                    pokemon['Image'] = f"Sprites/Pokemon/{image_filename}"  # Set anyway for consistency
        except Exception as e:
            print(f"✗ {name}: Error - {str(e)}")
            pokemon['Image'] = f"Sprites/Pokemon/{image_filename}"  # Set anyway for consistency
        
        # Be nice to the server
        time.sleep(0.5)
    
    # Update CSV with image column
    print("\n\nUpdating pokemon_gen1.csv with image filenames...")
    
    fieldnames = ['Number', 'Name', 'Type1', 'Type2', 'Rarity', 'Weight', 'Image']
    
    with open('pokemon_gen1.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(pokemon_list)
    
    print("✓ CSV updated successfully!")
    print(f"\nImages saved to: {images_dir.absolute()}")

if __name__ == "__main__":
    print("=== Pokémon Image Downloader ===\n")
    download_pokemon_sprites()
    print("\n=== Complete ===")

