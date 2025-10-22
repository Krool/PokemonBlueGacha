"""
Script to scrape Pokemon species, height, weight, and Pokedex entries from PokeAPI
"""
import requests
import csv
import time
from pathlib import Path

def get_pokemon_details(pokemon_id):
    """Fetch Pokemon details from PokeAPI"""
    try:
        # Get main Pokemon data
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
        response.raise_for_status()
        pokemon_data = response.json()
        
        # Get species data (for genus/species and Pokedex entries)
        species_response = requests.get(pokemon_data['species']['url'])
        species_response.raise_for_status()
        species_data = species_response.json()
        
        # Extract species name (genus)
        genus = None
        for genus_entry in species_data['genera']:
            if genus_entry['language']['name'] == 'en':
                # Remove " Pokémon" from the end
                genus = genus_entry['genus'].replace(' Pokémon', '').replace(' Pokemon', '')
                break
        
        # Extract Red/Blue Pokedex entry
        pokedex_entry = None
        for entry in species_data['flavor_text_entries']:
            if entry['language']['name'] == 'en' and entry['version']['name'] in ['red', 'blue']:
                # Clean up the text (remove newlines and form feeds)
                pokedex_entry = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ').strip()
                break
        
        # If no Red/Blue entry, try FireRed/LeafGreen
        if not pokedex_entry:
            for entry in species_data['flavor_text_entries']:
                if entry['language']['name'] == 'en' and entry['version']['name'] in ['firered', 'leafgreen']:
                    pokedex_entry = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ').strip()
                    break
        
        # Convert height from decimeters to feet (1 decimeter = 0.328084 feet)
        height_dm = pokemon_data['height']
        height_feet = height_dm * 0.328084
        
        # Convert weight from hectograms to pounds (1 hectogram = 0.220462 pounds)
        weight_hg = pokemon_data['weight']
        weight_lbs = weight_hg * 0.220462
        
        return {
            'name': pokemon_data['name'].capitalize(),
            'species': genus or 'Unknown',
            'height_ft': round(height_feet, 1),
            'weight_lbs': round(weight_lbs, 1),
            'pokedex_entry': pokedex_entry or 'No Pokedex entry available.'
        }
    except Exception as e:
        print(f"Error fetching Pokemon #{pokemon_id}: {e}")
        return None

def main():
    """Main function to scrape all Gen 1 Pokemon"""
    print("Starting Pokemon details scraping for Gen 1 (1-151)...")
    
    results = []
    
    # Gen 1 Pokemon: 1-151
    for i in range(1, 152):
        print(f"Fetching #{i:03d}...", end=' ')
        details = get_pokemon_details(i)
        
        if details:
            results.append({
                'number': f"{i:03d}",
                **details
            })
            print(f"[OK] {details['name']} - {details['species']}")
        else:
            print("[FAILED]")
        
        # Be nice to the API
        time.sleep(0.5)
    
    # Read existing pokemon CSV
    csv_path = Path(__file__).parent.parent / 'src' / 'data' / 'pokemon_gen1.csv'
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        existing_data = list(reader)
    
    # Merge new data with existing data
    for existing_row in existing_data:
        number = existing_row['Number']
        # Find matching scraped data
        for result in results:
            if result['number'] == number:
                existing_row['Species'] = result['species']
                existing_row['Height_ft'] = result['height_ft']
                existing_row['Weight_lbs'] = result['weight_lbs']
                existing_row['Pokedex_Entry'] = result['pokedex_entry']
                break
    
    # Write updated CSV
    output_path = Path(__file__).parent.parent / 'src' / 'data' / 'pokemon_gen1_updated.csv'
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['Number', 'Name', 'Type1', 'Type2', 'Rarity', 
                      'Red_Weight', 'Blue_Weight', 'Yellow_Weight', 'Image',
                      'Species', 'Height_ft', 'Weight_lbs', 'Pokedex_Entry']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_data)
    
    print(f"\n[OK] Complete! Updated CSV saved to: {output_path}")
    print(f"Total Pokemon processed: {len(results)}")

if __name__ == '__main__':
    main()

