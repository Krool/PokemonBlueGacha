"""
Gacha statistics calculations
"""
from typing import Dict, List, Tuple
import math


class GachaStats:
    """Calculate gacha statistics and expected pulls"""
    
    @staticmethod
    def calculate_expected_pulls_for_version(pokemon_list: List, rarities_dict: Dict, 
                                             version: str, owned_pokemon: Dict[str, int]) -> float:
        """
        Estimate pulls needed to get the least likely remaining Pokemon.
        Simplified: finds the rarest unowned Pokemon and estimates pulls needed.
        
        Args:
            pokemon_list: List of all Pokemon
            rarities_dict: Dictionary of rarity data
            version: "Red", "Blue", or "Yellow"
            owned_pokemon: Dict of owned Pokemon {number: count}
            
        Returns:
            Estimated number of pulls to get rarest Pokemon
        """
        # Filter Pokemon available in this version
        available_pokemon = [p for p in pokemon_list if p.get_weight_for_version(version) > 0]
        
        if not available_pokemon:
            return 0.0
        
        # Calculate rarity probabilities
        total_rarity_weight = sum(r.get_weight_for_version(version) 
                                  for r in rarities_dict.values())
        
        if total_rarity_weight == 0:
            return 0.0
        
        # Find the least likely unowned Pokemon
        min_probability = 1.0
        
        for pokemon in available_pokemon:
            # Skip if owned
            if pokemon.number in owned_pokemon:
                continue
            
            rarity = rarities_dict.get(pokemon.rarity)
            if not rarity:
                continue
            
            # Probability of this rarity
            rarity_prob = rarity.get_weight_for_version(version) / total_rarity_weight
            
            # Count Pokemon in same rarity (in this version)
            same_rarity_pokemon = [p for p in available_pokemon if p.rarity == pokemon.rarity]
            total_rarity_pokemon_weight = sum(p.get_weight_for_version(version) 
                                             for p in same_rarity_pokemon)
            
            if total_rarity_pokemon_weight == 0:
                continue
            
            # Probability within rarity
            within_rarity_prob = pokemon.get_weight_for_version(version) / total_rarity_pokemon_weight
            
            # Combined probability
            prob = rarity_prob * within_rarity_prob
            min_probability = min(min_probability, prob)
        
        # If all owned, return 0
        if min_probability == 1.0:
            return 0.0
        
        # Expected pulls to get the rarest Pokemon (1/probability)
        return 1.0 / min_probability
    
    @staticmethod
    def calculate_expected_pulls_from_scratch(pokemon_list: List, rarities_dict: Dict) -> float:
        """
        Calculate expected pulls to complete collection from scratch.
        Returns sum of expected pulls from all three versions.
        
        Args:
            pokemon_list: List of all Pokemon
            rarities_dict: Dictionary of rarity data
            
        Returns:
            Sum of expected pulls from all versions
        """
        versions = ["Red", "Blue", "Yellow"]
        total_expected = 0.0
        
        for version in versions:
            expected = GachaStats.calculate_expected_pulls_for_version(
                pokemon_list, rarities_dict, version, {}
            )
            total_expected += expected
        
        return total_expected
    
    @staticmethod
    def find_recommended_version(pokemon_list: List, rarities_dict: Dict, 
                                 owned_pokemon: Dict[str, int]) -> Tuple[str, float]:
        """
        Find which version needs the most pulls to complete.
        
        Args:
            pokemon_list: List of all Pokemon
            rarities_dict: Dictionary of rarity data
            owned_pokemon: Dict of owned Pokemon
            
        Returns:
            Tuple of (version_name, expected_pulls)
        """
        versions = ["Red", "Blue", "Yellow"]
        version_pulls = {}
        
        for version in versions:
            pulls = GachaStats.calculate_expected_pulls_for_version(
                pokemon_list, rarities_dict, version, owned_pokemon
            )
            version_pulls[version] = pulls
        
        # Return version with most pulls needed
        recommended = max(version_pulls, key=version_pulls.get)
        return recommended, version_pulls[recommended]
    
    @staticmethod
    def calculate_optimal_strategy_cost(pokemon_list: List, rarities_dict: Dict, 
                                       gacha_machines: Dict) -> int:
        """
        Calculate expected Pokédollar cost using optimal pull strategy.
        Strategy: Pull from Yellow for legendaries (best rate), then Red/Blue for exclusives.
        
        Args:
            pokemon_list: List of all Pokemon
            rarities_dict: Dictionary of rarity data
            gacha_machines: Dict of gacha machine data
            
        Returns:
            Expected total cost in Pokédollars (using 10-pulls)
        """
        # Count legendaries (only in Yellow effectively due to better rates)
        legendary_pokemon = [p for p in pokemon_list if p.rarity == "Legendary"]
        
        # Calculate expected pulls for legendaries from Yellow
        # Yellow has 2% legendary rate (weight 2 out of 100)
        yellow_legendary_weight = rarities_dict.get("Legendary").get_weight_for_version("Yellow")
        yellow_total_weight = sum(r.get_weight_for_version("Yellow") for r in rarities_dict.values())
        legendary_rate = yellow_legendary_weight / yellow_total_weight  # 2/100 = 0.02
        
        # Calculate probability for each legendary in Yellow
        yellow_legendaries = [p for p in legendary_pokemon if p.get_weight_for_version("Yellow") > 0]
        total_legendary_weight = sum(p.get_weight_for_version("Yellow") for p in yellow_legendaries)
        
        # Expected pulls for each legendary
        yellow_expected_pulls = 0.0
        for pokemon in yellow_legendaries:
            pokemon_prob = legendary_rate * (pokemon.get_weight_for_version("Yellow") / total_legendary_weight)
            yellow_expected_pulls += 1.0 / pokemon_prob
        
        # Count version exclusives (Pokemon with weight 0 in other versions)
        red_exclusives = [p for p in pokemon_list 
                         if p.get_weight_for_version("Red") > 0 
                         and p.get_weight_for_version("Blue") == 0 
                         and p.get_weight_for_version("Yellow") == 0]
        
        blue_exclusives = [p for p in pokemon_list 
                          if p.get_weight_for_version("Blue") > 0 
                          and p.get_weight_for_version("Red") == 0 
                          and p.get_weight_for_version("Yellow") == 0]
        
        # Estimate pulls for exclusives (rough estimate based on average probability)
        # Most exclusives are Common/Uncommon, so estimate ~50 pulls per exclusive
        red_expected_pulls = len(red_exclusives) * 50
        blue_expected_pulls = len(blue_exclusives) * 50
        
        # Get 10-pull costs
        yellow_cost_per_pull = gacha_machines["Yellow"].cost_10pull / 10
        red_cost_per_pull = gacha_machines["Red"].cost_10pull / 10
        blue_cost_per_pull = gacha_machines["Blue"].cost_10pull / 10
        
        # Calculate total cost
        total_cost = (
            yellow_expected_pulls * yellow_cost_per_pull +
            red_expected_pulls * red_cost_per_pull +
            blue_expected_pulls * blue_cost_per_pull
        )
        
        return int(total_cost)

