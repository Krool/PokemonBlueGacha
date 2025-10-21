#!/usr/bin/env python3
"""
Pokémon Blue Gacha - Drop Rate and Cost Analysis
Calculates expected pulls, costs, and probabilities for the gacha system.

Two-Step Weighted System:
1. Roll for rarity based on rarity_drop_weights.csv
2. Roll for Pokémon within that rarity based on individual weights in pokemon_gen1.csv
"""

import math
import csv
from pathlib import Path

class PokemonGachaCalculator:
    def __init__(self, pokemon_csv='pokemon_gen1.csv', rarity_csv='rarity_drop_weights.csv'):
        # Load rarity weights from CSV
        self.rarity_weights = self._load_rarity_weights(rarity_csv)
        
        # Load Pokémon data with individual weights
        self.pokemon_data = self._load_pokemon_data(pokemon_csv)
        
        # Calculate rarity counts and total weights
        self.rarity_counts = self._calculate_rarity_counts()
        self.rarity_total_weights = self._calculate_rarity_total_weights()
        
        # Calculate total rarity weight and probabilities
        self.total_rarity_weight = sum(self.rarity_weights.values())
        self.probabilities = self._calculate_probabilities()
        
        # Gacha pricing (to be set later)
        self.single_pull_cost = None
        self.ten_pull_cost = None
    
    def _load_rarity_weights(self, csv_path):
        """Load rarity weights from CSV file"""
        weights = {}
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rarity = row['Rarity'].lower()
                    weights[rarity] = int(row['Drop_Weight'])
        except FileNotFoundError:
            # Fallback to hardcoded values if file not found
            weights = {
                'common': 42,
                'uncommon': 36,
                'rare': 15,
                'epic': 6,
                'legendary': 1
            }
        return weights
    
    def _load_pokemon_data(self, csv_path):
        """Load Pokémon data with individual weights from CSV"""
        pokemon = []
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    pokemon.append({
                        'number': row['Number'],
                        'name': row['Name'],
                        'type1': row['Type1'],
                        'type2': row['Type2'],
                        'rarity': row['Rarity'].lower(),
                        'weight': float(row['Weight'])
                    })
        except FileNotFoundError:
            print(f"Warning: {csv_path} not found. Using default counts.")
            pokemon = []
        return pokemon
    
    def _calculate_rarity_counts(self):
        """Count Pokémon per rarity"""
        counts = {'common': 0, 'uncommon': 0, 'rare': 0, 'epic': 0, 'legendary': 0}
        for pokemon in self.pokemon_data:
            counts[pokemon['rarity']] += 1
        return counts
    
    def _calculate_rarity_total_weights(self):
        """Calculate total weight for each rarity tier"""
        totals = {'common': 0, 'uncommon': 0, 'rare': 0, 'epic': 0, 'legendary': 0}
        for pokemon in self.pokemon_data:
            totals[pokemon['rarity']] += pokemon['weight']
        return totals
        
    def _calculate_probabilities(self):
        """Calculate probabilities for the two-step weighted system"""
        probabilities = {}
        for rarity_name in self.rarity_weights:
            # Step 1: Probability of rolling this rarity
            rarity_prob = self.rarity_weights[rarity_name] / self.total_rarity_weight
            
            # Step 2: Average probability within the rarity (assumes uniform weight=1)
            # For weighted calculation, this is the probability of a weight-1 Pokémon
            total_weight = self.rarity_total_weights[rarity_name]
            if total_weight > 0:
                # Probability for a weight-1 Pokémon in this rarity
                base_individual_prob = rarity_prob / total_weight
            else:
                base_individual_prob = 0
            
            probabilities[rarity_name] = {
                'rarity_prob': rarity_prob,
                'base_individual': base_individual_prob,  # Probability for weight=1 Pokémon
                'total_rarity': rarity_prob,
                'count': self.rarity_counts[rarity_name],
                'total_weight': total_weight
            }
        return probabilities
    
    def get_pokemon_probability(self, pokemon_name):
        """Get the probability of pulling a specific Pokémon by name"""
        for pokemon in self.pokemon_data:
            if pokemon['name'].lower() == pokemon_name.lower():
                rarity = pokemon['rarity']
                rarity_prob = self.probabilities[rarity]['rarity_prob']
                total_weight = self.rarity_total_weights[rarity]
                individual_weight = pokemon['weight']
                return (rarity_prob * individual_weight) / total_weight
        return None
    
    def set_pricing(self, single_pull_cost=None, ten_pull_cost=None):
        """Set gacha pull pricing"""
        self.single_pull_cost = single_pull_cost
        self.ten_pull_cost = ten_pull_cost
    
    def expected_pulls_for_complete_collection(self):
        """Calculate expected number of pulls to collect all 151 Pokémon using weighted system"""
        total_expected = 0
        # Calculate expected pulls for each individual Pokémon
        for pokemon in self.pokemon_data:
            prob = self.get_pokemon_probability(pokemon['name'])
            if prob > 0:
                total_expected += 1 / prob
        return total_expected
    
    def expected_pulls_by_rarity(self):
        """Calculate expected pulls per Pokémon by rarity using weighted system"""
        results = {}
        for rarity_name in self.rarity_weights:
            prob_data = self.probabilities[rarity_name]
            # For weight=1 Pokémon
            base_prob = prob_data['base_individual']
            results[rarity_name] = {
                'pulls_per_pokemon_weight1': 1 / base_prob if base_prob > 0 else 0,
                'base_probability_percent': base_prob * 100,
                'rarity_probability_percent': prob_data['rarity_prob'] * 100,
                'total_rarity_percent': prob_data['total_rarity'] * 100,
                'total_weight': prob_data['total_weight']
            }
        return results
    
    def expected_cost_for_complete_collection(self):
        """Calculate expected cost to collect all Pokémon"""
        if not self.ten_pull_cost:
            return None
            
        total_pulls = self.expected_pulls_for_complete_collection()
        # Assume optimal strategy of always doing 10-pulls
        ten_pulls_needed = math.ceil(total_pulls / 10)
        return ten_pulls_needed * self.ten_pull_cost
    
    def probability_of_specific_pokemon(self, rarity, weight=1):
        """Get probability of pulling a Pokémon of given rarity and weight"""
        if rarity not in self.probabilities:
            return None
        rarity_prob = self.probabilities[rarity]['rarity_prob']
        total_weight = self.rarity_total_weights[rarity]
        if total_weight > 0:
            return (rarity_prob * weight) / total_weight
        return None
    
    def expected_pulls_for_specific_pokemon(self, rarity, weight=1):
        """Expected pulls to get a Pokémon of given rarity and weight"""
        prob = self.probability_of_specific_pokemon(rarity, weight)
        if prob:
            return 1 / prob
        return None
    
    def print_complete_analysis(self):
        """Print comprehensive gacha analysis using two-step weighted system"""
        print("=== POKÉMON BLUE GACHA ANALYSIS (Two-Step Weighted System) ===\n")
        print("Step 1: Roll for rarity based on rarity weights")
        print("Step 2: Weighted selection within rarity tier\n")
        
        print(f"Total rarity weight: {self.total_rarity_weight:,}")
        print(f"Total Pokémon: {sum(self.rarity_counts.values())}\n")
        
        print("RARITY BREAKDOWN:")
        print("-" * 100)
        print(f"{'Rarity':<10} | {'Count':>5} | {'Rarity %':>8} | {'Weight=1 Prob':>14} | {'Pulls (W=1)':>12} | {'Total Wgt':>10}")
        print("-" * 100)
        
        rarity_analysis = self.expected_pulls_by_rarity()
        for rarity_name, data in rarity_analysis.items():
            count = self.rarity_counts[rarity_name]
            print(f"{rarity_name.upper():<10} | {count:>5} | "
                  f"{data['rarity_probability_percent']:>7.2f}% | "
                  f"{data['base_probability_percent']:>13.4f}% | "
                  f"{data['pulls_per_pokemon_weight1']:>12.0f} | "
                  f"{data['total_weight']:>10.1f}")
        
        print(f"\nEXPECTED PULLS FOR COMPLETE COLLECTION:")
        total_expected = self.expected_pulls_for_complete_collection()
        print(f"Total expected pulls (all weights at 1): {total_expected:,.0f}")
        
        if self.ten_pull_cost:
            total_cost = self.expected_cost_for_complete_collection()
            print(f"Expected cost (10-pulls @ ${self.ten_pull_cost}): ${total_cost:,.2f}")
        
        print(f"\nWEIGHT EXAMPLES:")
        print("If a Pokémon has weight 2, it's 2x more likely than weight-1 Pokémon in same rarity")
        print("If a Pokémon has weight 0.5, it's 0.5x (half) as likely as weight-1 Pokémon")
        
        print(f"\nLEGENDARY ANALYSIS (assuming all weights = 1):")
        legendary_prob = self.probability_of_specific_pokemon('legendary', weight=1)
        legendary_rarity_prob = self.probabilities['legendary']['rarity_prob']
        print(f"Chance to roll Legendary rarity: {legendary_rarity_prob:.6f} ({legendary_rarity_prob*100:.2f}%)")
        print(f"Chance for specific legendary (weight=1): {legendary_prob:.6f} ({legendary_prob*100:.4f}%)")
        print(f"Expected pulls for specific legendary: {1/legendary_prob:,.0f}")
        print(f"Expected pulls for any legendary: {1/legendary_rarity_prob:,.0f}")

def main():
    """Run the gacha analysis"""
    calculator = PokemonGachaCalculator()
    
    # Set example pricing (can be updated later)
    # calculator.set_pricing(single_pull_cost=1.00, ten_pull_cost=9.00)
    
    calculator.print_complete_analysis()

if __name__ == "__main__":
    main()
