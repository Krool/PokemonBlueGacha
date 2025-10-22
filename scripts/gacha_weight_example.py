#!/usr/bin/env python3
"""
Example demonstrating how individual Pokémon weights work in the gacha system
"""

from gacha_calculations import PokemonGachaCalculator

def main():
    calc = PokemonGachaCalculator()
    
    print("=== WEIGHT SYSTEM EXAMPLES ===\n")
    
    # Example 1: All weights = 1 (current default)
    print("EXAMPLE 1: All Uncommon Pokémon have weight = 1")
    print(f"  Total Uncommon weight: 52")
    print(f"  Chance for any specific Uncommon: 36% ÷ 52 = 0.692%")
    bulbasaur_prob = calc.get_pokemon_probability("Bulbasaur")
    print(f"  Bulbasaur probability: {bulbasaur_prob*100:.4f}%")
    print(f"  Expected pulls for Bulbasaur: {1/bulbasaur_prob:.0f}\n")
    
    # Example 2: What if Bulbasaur had weight = 2?
    print("EXAMPLE 2: If Bulbasaur had weight = 2 (others = 1)")
    print(f"  Total Uncommon weight would be: 53 (51×1 + 1×2)")
    print(f"  Bulbasaur chance: (36% × 2) ÷ 53 = 1.358%")
    bulbasaur_weight2_prob = calc.probability_of_specific_pokemon('uncommon', weight=2)
    print(f"  Calculated probability: {bulbasaur_weight2_prob*100:.4f}%")
    print(f"  Expected pulls: {1/bulbasaur_weight2_prob:.0f}")
    print(f"  This is {bulbasaur_weight2_prob / bulbasaur_prob:.2f}x more likely!\n")
    
    # Example 3: Featured Pokémon with high weight
    print("EXAMPLE 3: 'Featured' Pikachu (Rare) with weight = 5")
    print(f"  Normal Rare weight total: 35 (all weight=1)")
    print(f"  With Pikachu at weight=5: 39 (34×1 + 1×5)")
    pikachu_featured_prob = (0.15 * 5) / 39  # 15% rarity chance, weight 5, total 39
    print(f"  Pikachu chance: (15% × 5) ÷ 39 = {pikachu_featured_prob*100:.4f}%")
    print(f"  Expected pulls: {1/pikachu_featured_prob:.0f}")
    
    normal_rare_prob = calc.probability_of_specific_pokemon('rare', weight=1)
    print(f"  Normal rare Pokémon (weight=1): {normal_rare_prob*100:.4f}%")
    print(f"  Featured Pikachu is {pikachu_featured_prob/normal_rare_prob:.2f}x more likely!\n")
    
    # Example 4: Legendary weights
    print("EXAMPLE 4: Legendary Pokémon (all weight=1)")
    print(f"  Legendary rarity chance: 1.00%")
    print(f"  Total legendary weight: 5")
    print(f"  Each legendary: 1% ÷ 5 = 0.20%")
    mewtwo_prob = calc.get_pokemon_probability("Mewtwo")
    print(f"  Mewtwo probability: {mewtwo_prob*100:.4f}%")
    print(f"  Expected pulls: {1/mewtwo_prob:.0f}")
    print(f"  1 in {1/mewtwo_prob:.0f} pulls will be Mewtwo\n")

if __name__ == "__main__":
    main()

