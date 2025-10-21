"""
Gacha roll logic with two-step weighted system
"""
import random
from typing import List, Dict
from data.pokemon_data import Pokemon
from data.rarity_data import Rarity


class GachaSystem:
    """Handles gacha rolling logic"""
    
    def __init__(self, pokemon_list: List[Pokemon], rarities_dict: Dict[str, Rarity]):
        """
        Initialize gacha system
        
        Args:
            pokemon_list: List of all Pokemon
            rarities_dict: Dictionary of rarity definitions
        """
        self.pokemon_list = pokemon_list
        self.rarities_dict = rarities_dict
    
    def roll_single(self, version: str) -> Pokemon:
        """
        Perform a single gacha roll for the specified version
        
        Two-step process:
        1. Roll on rarity weights to determine rarity tier
        2. Roll on Pokemon weights within that rarity for specific Pokemon
        
        Args:
            version: "Red", "Blue", or "Yellow"
            
        Returns:
            Rolled Pokemon
        """
        # Step 1: Determine rarity tier
        rarity_name = self._roll_rarity(version)
        
        # Step 2: Roll specific Pokemon from that rarity
        pokemon = self._roll_pokemon_from_rarity(version, rarity_name)
        
        return pokemon
    
    def roll_ten(self, version: str) -> List[Pokemon]:
        """
        Perform 10 gacha rolls
        
        Args:
            version: "Red", "Blue", or "Yellow"
            
        Returns:
            List of 10 rolled Pokemon
        """
        return [self.roll_single(version) for _ in range(10)]
    
    def _roll_rarity(self, version: str) -> str:
        """
        Roll to determine rarity tier based on version weights
        
        Args:
            version: "Red", "Blue", or "Yellow"
            
        Returns:
            Rarity name (e.g., "Common", "Legendary")
        """
        # Build weighted list of rarities
        rarity_choices = []
        rarity_weights = []
        
        for rarity_name, rarity_obj in self.rarities_dict.items():
            weight = rarity_obj.get_weight_for_version(version)
            if weight > 0:
                rarity_choices.append(rarity_name)
                rarity_weights.append(weight)
        
        # Perform weighted random choice
        chosen_rarity = random.choices(rarity_choices, weights=rarity_weights, k=1)[0]
        return chosen_rarity
    
    def _roll_pokemon_from_rarity(self, version: str, rarity: str) -> Pokemon:
        """
        Roll a specific Pokemon from the given rarity tier
        
        Args:
            version: "Red", "Blue", or "Yellow"
            rarity: Rarity tier name
            
        Returns:
            Rolled Pokemon
        """
        # Filter Pokemon by rarity and version availability
        eligible_pokemon = []
        pokemon_weights = []
        
        for pokemon in self.pokemon_list:
            if pokemon.rarity == rarity:
                weight = pokemon.get_weight_for_version(version)
                if weight > 0:
                    eligible_pokemon.append(pokemon)
                    pokemon_weights.append(weight)
        
        # Sanity check
        if not eligible_pokemon:
            raise ValueError(f"No eligible Pokemon found for rarity '{rarity}' in version '{version}'")
        
        # Perform weighted random choice
        chosen_pokemon = random.choices(eligible_pokemon, weights=pokemon_weights, k=1)[0]
        return chosen_pokemon
    
    def get_rarity_probabilities(self, version: str) -> Dict[str, float]:
        """
        Calculate probability of each rarity tier for a version
        
        Args:
            version: "Red", "Blue", or "Yellow"
            
        Returns:
            Dictionary mapping rarity name to probability (0.0 to 1.0)
        """
        total_weight = sum(
            rarity.get_weight_for_version(version) 
            for rarity in self.rarities_dict.values()
        )
        
        probabilities = {}
        for rarity_name, rarity_obj in self.rarities_dict.items():
            weight = rarity_obj.get_weight_for_version(version)
            probabilities[rarity_name] = weight / total_weight if total_weight > 0 else 0.0
        
        return probabilities
    
    def get_pokemon_probability(self, pokemon: Pokemon, version: str) -> float:
        """
        Calculate the probability of rolling a specific Pokemon
        
        Args:
            pokemon: Pokemon to calculate probability for
            version: "Red", "Blue", or "Yellow"
            
        Returns:
            Probability as a float (0.0 to 1.0)
        """
        # Get rarity probability
        rarity_probs = self.get_rarity_probabilities(version)
        rarity_prob = rarity_probs.get(pokemon.rarity, 0.0)
        
        # Get Pokemon's weight within its rarity
        pokemon_weight = pokemon.get_weight_for_version(version)
        if pokemon_weight == 0:
            return 0.0
        
        # Calculate total weight of all Pokemon in this rarity for this version
        total_rarity_weight = sum(
            p.get_weight_for_version(version)
            for p in self.pokemon_list
            if p.rarity == pokemon.rarity
        )
        
        # Pokemon probability = rarity_prob * (pokemon_weight / total_rarity_weight)
        if total_rarity_weight > 0:
            pokemon_prob_in_rarity = pokemon_weight / total_rarity_weight
            return rarity_prob * pokemon_prob_in_rarity
        else:
            return 0.0

