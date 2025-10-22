"""
Items Gacha Logic - Two-step weighted system for item drops
"""
import random
from typing import List, Dict


def perform_items_gacha(items_list: List, rarities_dict: Dict, count: int = 1) -> List[str]:
    """
    Perform items gacha pull(s) using two-step weighted system
    
    Step 1: Roll for rarity tier based on rarity weights
    Step 2: Roll for specific item within that rarity based on item weights
    
    Args:
        items_list: List of all Item objects
        rarities_dict: Dictionary of rarity name -> Rarity object
        count: Number of pulls (1 or 10)
        
    Returns:
        List of item numbers (e.g., ["001", "023", ...])
    """
    results = []
    
    for _ in range(count):
        # Step 1: Roll for rarity
        rarity_name = _roll_for_rarity(rarities_dict)
        
        # Step 2: Roll for item within that rarity
        item = _roll_for_item_in_rarity(items_list, rarity_name)
        
        if item:
            results.append(item.number)
        else:
            print(f"Warning: No item found for rarity {rarity_name}")
    
    return results


def _roll_for_rarity(rarities_dict: Dict) -> str:
    """
    Roll for rarity tier using rarity weights
    
    Args:
        rarities_dict: Dictionary of rarity name -> Rarity object
        
    Returns:
        Rarity name (e.g., "Common", "Legendary")
    """
    # Build weighted list
    rarity_weights = []
    rarity_names = []
    
    for rarity_name, rarity in rarities_dict.items():
        # Items use the Items_Weight from the rarity CSV
        weight = rarity.get_weight_for_version("Items")
        rarity_weights.append(weight)
        rarity_names.append(rarity_name)
    
    # Weighted random choice
    chosen_rarity = random.choices(rarity_names, weights=rarity_weights, k=1)[0]
    return chosen_rarity


def _roll_for_item_in_rarity(items_list: List, rarity_name: str):
    """
    Roll for specific item within a rarity tier
    
    Args:
        items_list: List of all Item objects
        rarity_name: Rarity to roll from
        
    Returns:
        Item object, or None if no items found
    """
    # Filter items by rarity
    items_in_rarity = [item for item in items_list if item.rarity == rarity_name]
    
    if not items_in_rarity:
        return None
    
    # Build weighted list
    item_weights = [item.weight for item in items_in_rarity]
    
    # Weighted random choice
    chosen_item = random.choices(items_in_rarity, weights=item_weights, k=1)[0]
    return chosen_item


def calculate_item_drop_rate(item, items_list: List, rarities_dict: Dict) -> float:
    """
    Calculate drop rate percentage for a specific item
    
    Args:
        item: Item object
        items_list: List of all Item objects
        rarities_dict: Dictionary of rarity name -> Rarity object
        
    Returns:
        Drop rate as percentage (e.g., 0.5432 for 0.5432%)
    """
    # Get total rarity weight for Items gacha
    total_rarity_weight = sum(
        rarity.get_weight_for_version("Items")
        for rarity in rarities_dict.values()
    )
    
    if total_rarity_weight == 0:
        return 0.0
    
    # Get this item's rarity
    rarity = rarities_dict.get(item.rarity)
    if not rarity:
        return 0.0
    
    rarity_weight = rarity.get_weight_for_version("Items")
    
    # Probability of this rarity
    rarity_prob = rarity_weight / total_rarity_weight
    
    # Get all items in same rarity
    items_in_rarity = [i for i in items_list if i.rarity == item.rarity]
    total_rarity_item_weight = sum(i.weight for i in items_in_rarity)
    
    if total_rarity_item_weight == 0:
        return 0.0
    
    # Probability within rarity
    within_rarity_prob = item.weight / total_rarity_item_weight
    
    # Combined probability as percentage
    return (rarity_prob * within_rarity_prob) * 100


def calculate_expected_value(items_list: List, rarities_dict: Dict) -> float:
    """
    Calculate expected Pokédollar value per pull
    
    Formula: Sum of (item_value × drop_probability) for all items
    
    Args:
        items_list: List of all Item objects
        rarities_dict: Dictionary of rarity name -> Rarity object
        
    Returns:
        Expected value in Pokédollars
    """
    expected_value = 0.0
    
    for item in items_list:
        drop_rate_percent = calculate_item_drop_rate(item, items_list, rarities_dict)
        drop_probability = drop_rate_percent / 100.0  # Convert to 0.0-1.0 range
        expected_value += item.value * drop_probability
    
    return expected_value


def calculate_new_item_chance(items_list: List, rarities_dict: Dict, owned_items: Dict[str, int]) -> float:
    """
    Calculate percentage chance of getting a new (unowned) item
    
    Args:
        items_list: List of all Item objects
        rarities_dict: Dictionary of rarity name -> Rarity object
        owned_items: Dictionary of owned item numbers
        
    Returns:
        Percentage chance (0-100)
    """
    total_new_chance = 0.0
    
    for item in items_list:
        if item.number not in owned_items:
            drop_rate = calculate_item_drop_rate(item, items_list, rarities_dict)
            total_new_chance += drop_rate
    
    return total_new_chance

