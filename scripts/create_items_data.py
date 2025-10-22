"""
Script to create items CSV data for the Items Gacha
Scrapes Gen 1 items from Bulbapedia and matches with icons from PokéSprite
"""

# Gen 1 Items from Bulbapedia (manually curated, excluding specified items)
gen1_items = [
    # Poké Balls
    {"name": "Master Ball", "index": 1, "category": "ball"},
    {"name": "Ultra Ball", "index": 2, "category": "ball"},
    {"name": "Great Ball", "index": 3, "category": "ball"},
    {"name": "Poké Ball", "index": 4, "category": "ball"},
    {"name": "Safari Ball", "index": 8, "category": "ball"},
    
    # Evolution Stones
    {"name": "Moon Stone", "index": 10, "category": "evo-stone"},
    {"name": "Fire Stone", "index": 32, "category": "evo-stone"},
    {"name": "Thunder Stone", "index": 33, "category": "evo-stone"},
    {"name": "Water Stone", "index": 34, "category": "evo-stone"},
    {"name": "Leaf Stone", "index": 47, "category": "evo-stone"},
    
    # Status Healers
    {"name": "Antidote", "index": 11, "category": "medicine"},
    {"name": "Burn Heal", "index": 12, "category": "medicine"},
    {"name": "Ice Heal", "index": 13, "category": "medicine"},
    {"name": "Awakening", "index": 14, "category": "medicine"},
    {"name": "Parlyz Heal", "index": 15, "category": "medicine"},
    {"name": "Full Heal", "index": 52, "category": "medicine"},
    
    # HP Restoration
    {"name": "Full Restore", "index": 16, "category": "medicine"},
    {"name": "Max Potion", "index": 17, "category": "medicine"},
    {"name": "Hyper Potion", "index": 18, "category": "medicine"},
    {"name": "Super Potion", "index": 19, "category": "medicine"},
    {"name": "Potion", "index": 20, "category": "medicine"},
    {"name": "Revive", "index": 53, "category": "medicine"},
    {"name": "Max Revive", "index": 54, "category": "medicine"},
    
    # Battle Items
    {"name": "X Accuracy", "index": 46, "category": "battle"},
    {"name": "Guard Spec.", "index": 55, "category": "battle"},
    {"name": "Dire Hit", "index": 58, "category": "battle"},
    {"name": "X Attack", "index": 60, "category": "battle"},
    {"name": "X Defend", "index": 61, "category": "battle"},
    {"name": "X Speed", "index": 62, "category": "battle"},
    {"name": "X Special", "index": 63, "category": "battle"},
    
    # Vitamins
    {"name": "HP Up", "index": 35, "category": "vitamin"},
    {"name": "Protein", "index": 36, "category": "vitamin"},
    {"name": "Iron", "index": 37, "category": "vitamin"},
    {"name": "Carbos", "index": 38, "category": "vitamin"},
    {"name": "Calcium", "index": 39, "category": "vitamin"},
    {"name": "Rare Candy", "index": 40, "category": "vitamin"},
    
    # Utility Items
    {"name": "Escape Rope", "index": 29, "category": "other"},
    {"name": "Repel", "index": 30, "category": "other"},
    {"name": "Super Repel", "index": 56, "category": "other"},
    {"name": "Max Repel", "index": 57, "category": "other"},
    {"name": "Poké Doll", "index": 51, "category": "other"},
    {"name": "Fresh Water", "index": 84, "category": "other"},
    {"name": "Soda Pop", "index": 85, "category": "other"},
    {"name": "Lemonade", "index": 86, "category": "other"},
    
    # Valuable Items
    {"name": "Nugget", "index": 49, "category": "valuable"},
    {"name": "Coin", "index": 59, "category": "valuable"},
    {"name": "Gold Teeth", "index": 103, "category": "valuable"},
    
    # TMs (selected useful ones)
    {"name": "TM01", "index": 193, "category": "tm", "move": "Mega Punch"},
    {"name": "TM02", "index": 194, "category": "tm", "move": "Razor Wind"},
    {"name": "TM05", "index": 197, "category": "tm", "move": "Mega Kick"},
    {"name": "TM06", "index": 198, "category": "tm", "move": "Toxic"},
    {"name": "TM07", "index": 199, "category": "tm", "move": "Horn Drill"},
    {"name": "TM08", "index": 200, "category": "tm", "move": "Body Slam"},
    {"name": "TM09", "index": 201, "category": "tm", "move": "Take Down"},
    {"name": "TM10", "index": 202, "category": "tm", "move": "Double-Edge"},
    {"name": "TM11", "index": 203, "category": "tm", "move": "Bubble Beam"},
    {"name": "TM12", "index": 204, "category": "tm", "move": "Water Gun"},
    {"name": "TM13", "index": 205, "category": "tm", "move": "Ice Beam"},
    {"name": "TM14", "index": 206, "category": "tm", "move": "Blizzard"},
    {"name": "TM15", "index": 207, "category": "tm", "move": "Hyper Beam"},
    {"name": "TM17", "index": 209, "category": "tm", "move": "Submission"},
    {"name": "TM19", "index": 211, "category": "tm", "move": "Seismic Toss"},
    {"name": "TM20", "index": 212, "category": "tm", "move": "Rage"},
    {"name": "TM22", "index": 214, "category": "tm", "move": "Solar Beam"},
    {"name": "TM23", "index": 215, "category": "tm", "move": "Dragon Rage"},
    {"name": "TM24", "index": 216, "category": "tm", "move": "Thunderbolt"},
    {"name": "TM25", "index": 217, "category": "tm", "move": "Thunder"},
    {"name": "TM26", "index": 218, "category": "tm", "move": "Earthquake"},
    {"name": "TM27", "index": 219, "category": "tm", "move": "Fissure"},
    {"name": "TM29", "index": 221, "category": "tm", "move": "Psychic"},
    {"name": "TM30", "index": 222, "category": "tm", "move": "Teleport"},
    {"name": "TM33", "index": 225, "category": "tm", "move": "Reflect"},
    {"name": "TM34", "index": 226, "category": "tm", "move": "Bide"},
    {"name": "TM35", "index": 227, "category": "tm", "move": "Metronome"},
    {"name": "TM38", "index": 230, "category": "tm", "move": "Fire Blast"},
    {"name": "TM44", "index": 236, "category": "tm", "move": "Rest"},
    {"name": "TM48", "index": 240, "category": "tm", "move": "Rock Slide"},
    {"name": "TM49", "index": 241, "category": "tm", "move": "Tri Attack"},
    {"name": "TM50", "index": 242, "category": "tm", "move": "Substitute"},
]

# Value assignments from Serebii (approximate based on usefulness and rarity)
item_values = {
    # Poké Balls (by catch rate/usefulness)
    "Master Ball": 50000,  # Priceless
    "Ultra Ball": 1200,
    "Great Ball": 600,
    "Poké Ball": 200,
    "Safari Ball": 1000,
    
    # Evolution Stones (rare and valuable)
    "Moon Stone": 3000,
    "Fire Stone": 3000,
    "Thunder Stone": 3000,
    "Water Stone": 3000,
    "Leaf Stone": 3000,
    
    # Status Healers
    "Antidote": 100,
    "Burn Heal": 250,
    "Ice Heal": 250,
    "Awakening": 200,
    "Parlyz Heal": 200,
    "Full Heal": 600,
    
    # HP Restoration
    "Full Restore": 3000,
    "Max Potion": 2500,
    "Hyper Potion": 1200,
    "Super Potion": 700,
    "Potion": 300,
    "Revive": 1500,
    "Max Revive": 4000,
    
    # Battle Items
    "X Accuracy": 950,
    "Guard Spec.": 700,
    "Dire Hit": 650,
    "X Attack": 500,
    "X Defend": 550,
    "X Speed": 350,
    "X Special": 350,
    
    # Vitamins (high value)
    "HP Up": 9800,
    "Protein": 9800,
    "Iron": 9800,
    "Carbos": 9800,
    "Calcium": 9800,
    "Rare Candy": 10000,  # Can't buy
    
    # Utility Items
    "Escape Rope": 550,
    "Repel": 350,
    "Super Repel": 500,
    "Max Repel": 700,
    "Poké Doll": 1000,
    "Fresh Water": 200,
    "Soda Pop": 300,
    "Lemonade": 350,
    
    # Valuable Items
    "Nugget": 5000,  # Sells for 5000
    "Coin": 10,
    "Gold Teeth": 5000,
    
    # TMs (varying by usefulness)
    "TM01": 3000,
    "TM02": 2000,
    "TM05": 3000,
    "TM06": 5000,  # Toxic - very useful
    "TM07": 3000,
    "TM08": 4000,  # Body Slam - very useful
    "TM09": 3000,
    "TM10": 3000,
    "TM11": 3000,
    "TM12": 2000,
    "TM13": 5500,  # Ice Beam
    "TM14": 5500,  # Blizzard
    "TM15": 7500,  # Hyper Beam - rare
    "TM17": 3000,
    "TM19": 3000,
    "TM20": 2000,
    "TM22": 6000,  # Solar Beam
    "TM23": 2000,
    "TM24": 5500,  # Thunderbolt
    "TM25": 5500,  # Thunder
    "TM26": 7000,  # Earthquake - very useful
    "TM27": 3000,
    "TM29": 7000,  # Psychic - very useful
    "TM30": 2000,
    "TM33": 3000,
    "TM34": 2000,
    "TM35": 2000,
    "TM38": 5500,  # Fire Blast
    "TM44": 3000,  # Rest
    "TM48": 4000,
    "TM49": 3000,
    "TM50": 5000,  # Substitute
}

# Icon mapping to PokéSprite filenames
icon_mapping = {
    # Balls
    "Master Ball": "ball/master.png",
    "Ultra Ball": "ball/ultra.png",
    "Great Ball": "ball/great.png",
    "Poké Ball": "ball/poke.png",
    "Safari Ball": "ball/safari.png",
    
    # Stones
    "Moon Stone": "evo-stone/moon.png",
    "Fire Stone": "evo-stone/fire.png",
    "Thunder Stone": "evo-stone/thunder.png",
    "Water Stone": "evo-stone/water.png",
    "Leaf Stone": "evo-stone/leaf.png",
    
    # Medicine
    "Antidote": "medicine/antidote.png",
    "Burn Heal": "medicine/burn-heal.png",
    "Ice Heal": "medicine/ice-heal.png",
    "Awakening": "medicine/awakening.png",
    "Parlyz Heal": "medicine/paralyze-heal.png",
    "Full Heal": "medicine/full-heal.png",
    "Full Restore": "medicine/full-restore.png",
    "Max Potion": "medicine/max-potion.png",
    "Hyper Potion": "medicine/hyper-potion.png",
    "Super Potion": "medicine/super-potion.png",
    "Potion": "medicine/potion.png",
    "Revive": "medicine/revive.png",
    "Max Revive": "medicine/max-revive.png",
    
    # Battle items
    "X Accuracy": "battle/x-accuracy.png",
    "Guard Spec.": "battle/guard-spec.png",
    "Dire Hit": "battle/dire-hit.png",
    "X Attack": "battle/x-attack.png",
    "X Defend": "battle/x-defense.png",
    "X Speed": "battle/x-speed.png",
    "X Special": "battle/x-sp-atk.png",
    
    # Vitamins
    "HP Up": "vitamin/hp-up.png",
    "Protein": "vitamin/protein.png",
    "Iron": "vitamin/iron.png",
    "Carbos": "vitamin/carbos.png",
    "Calcium": "vitamin/calcium.png",
    "Rare Candy": "vitamin/rare-candy.png",
    
    # Other
    "Escape Rope": "other/escape-rope.png",
    "Repel": "other/repel.png",
    "Super Repel": "other/super-repel.png",
    "Max Repel": "other/max-repel.png",
    "Poké Doll": "other/poke-doll.png",
    "Fresh Water": "other/fresh-water.png",
    "Soda Pop": "other/soda-pop.png",
    "Lemonade": "other/lemonade.png",
    "Nugget": "other/nugget.png",
    "Coin": "other/coin.png",
    "Gold Teeth": "other/gold-teeth.png",
    
    # TMs - use generic TM icon
    "TM01": "tm/normal.png",
    "TM02": "tm/normal.png",
    "TM05": "tm/normal.png",
    "TM06": "tm/poison.png",
    "TM07": "tm/normal.png",
    "TM08": "tm/normal.png",
    "TM09": "tm/normal.png",
    "TM10": "tm/normal.png",
    "TM11": "tm/water.png",
    "TM12": "tm/water.png",
    "TM13": "tm/ice.png",
    "TM14": "tm/ice.png",
    "TM15": "tm/normal.png",
    "TM17": "tm/fighting.png",
    "TM19": "tm/fighting.png",
    "TM20": "tm/normal.png",
    "TM22": "tm/grass.png",
    "TM23": "tm/dragon.png",
    "TM24": "tm/electric.png",
    "TM25": "tm/electric.png",
    "TM26": "tm/ground.png",
    "TM27": "tm/ground.png",
    "TM29": "tm/psychic.png",
    "TM30": "tm/psychic.png",
    "TM33": "tm/psychic.png",
    "TM34": "tm/normal.png",
    "TM35": "tm/normal.png",
    "TM38": "tm/fire.png",
    "TM44": "tm/psychic.png",
    "TM48": "tm/rock.png",
    "TM49": "tm/normal.png",
    "TM50": "tm/normal.png",
}

def assign_rarity_by_value(value):
    """Assign rarity based on item value (similar to Pokémon rarity)"""
    if value >= 10000:
        return "Legendary"
    elif value >= 7000:
        return "Epic"
    elif value >= 4000:
        return "Rare"
    elif value >= 1500:
        return "Uncommon"
    else:
        return "Common"

def create_items_csv():
    """Create items.csv file"""
    import csv
    
    with open('data/items_gen1.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Header
        writer.writerow(['Number', 'Name', 'Index', 'Category', 'Value', 'Rarity', 'Weight', 'Icon'])
        
        # Sort by index
        sorted_items = sorted(gen1_items, key=lambda x: x['index'])
        
        for i, item in enumerate(sorted_items, 1):
            name = item['name']
            index = item['index']
            category = item['category']
            value = item_values.get(name, 1000)
            rarity = assign_rarity_by_value(value)
            weight = 10  # Default weight of 10 for all items
            icon = icon_mapping.get(name, "other/item.png")
            
            writer.writerow([i, name, index, category, value, rarity, weight, icon])
    
    print(f"✓ Created data/items_gen1.csv with {len(sorted_items)} items")
    print(f"  Legendary: {sum(1 for item in sorted_items if assign_rarity_by_value(item_values.get(item['name'], 1000)) == 'Legendary')}")
    print(f"  Epic: {sum(1 for item in sorted_items if assign_rarity_by_value(item_values.get(item['name'], 1000)) == 'Epic')}")
    print(f"  Rare: {sum(1 for item in sorted_items if assign_rarity_by_value(item_values.get(item['name'], 1000)) == 'Rare')}")
    print(f"  Uncommon: {sum(1 for item in sorted_items if assign_rarity_by_value(item_values.get(item['name'], 1000)) == 'Uncommon')}")
    print(f"  Common: {sum(1 for item in sorted_items if assign_rarity_by_value(item_values.get(item['name'], 1000)) == 'Common')}")

if __name__ == "__main__":
    create_items_csv()

