"""
Game session data management
"""
from typing import Dict
from .save_manager import SaveManager


class GameData:
    """Manages current game session data"""
    
    def __init__(self, save_manager: SaveManager):
        self.save_manager = save_manager
        save_data = save_manager.load_game()
        
        # Load saved data
        self.gold: int = save_data['gold']
        self.pokemon_owned: Dict[str, int] = save_data['pokemon_owned']
        self.items_owned: Dict[str, int] = save_data.get('items_owned', {})
        self.newly_acquired: list = save_data['newly_acquired']
        self.newly_acquired_items: list = save_data.get('newly_acquired_items', [])
        self.stats: dict = save_data['stats']
        self.collection_complete_sound_played: bool = save_data.get('collection_complete_sound_played', False)
        self.music_muted: bool = save_data.get('music_muted', False)
    
    def save(self) -> bool:
        """
        Save current game state
        
        Returns:
            True if save successful
        """
        return self.save_manager.save_game(
            self.gold, 
            self.pokemon_owned,
            self.items_owned,
            self.newly_acquired,
            self.newly_acquired_items,
            self.stats,
            self.collection_complete_sound_played,
            self.music_muted
        )
    
    def add_gold(self, amount: int):
        """Add gold to player balance"""
        self.gold += amount
    
    def spend_gold(self, amount: int) -> bool:
        """
        Spend gold if player has enough
        
        Args:
            amount: Amount to spend
            
        Returns:
            True if purchase successful, False if not enough gold
        """
        if self.gold >= amount:
            self.gold -= amount
            self.stats['total_spent'] += amount
            return True
        return False
    
    def can_afford(self, amount: int) -> bool:
        """Check if player can afford a purchase"""
        return self.gold >= amount
    
    def add_pokemon(self, pokemon_number: str) -> bool:
        """
        Add a Pokémon to inventory
        
        Args:
            pokemon_number: Pokemon number (e.g., "001")
            
        Returns:
            True if this is a new Pokemon, False if already owned
        """
        is_new = pokemon_number not in self.pokemon_owned
        
        if is_new:
            self.pokemon_owned[pokemon_number] = 1
            self.newly_acquired.append(pokemon_number)
        else:
            self.pokemon_owned[pokemon_number] += 1
        
        return is_new
    
    def get_pokemon_count(self, pokemon_number: str) -> int:
        """Get count of owned Pokemon"""
        return self.pokemon_owned.get(pokemon_number, 0)
    
    def has_pokemon(self, pokemon_number: str) -> bool:
        """Check if player owns this Pokemon"""
        return pokemon_number in self.pokemon_owned
    
    def is_newly_acquired(self, pokemon_number: str) -> bool:
        """Check if Pokemon is newly acquired (for NEW badge)"""
        return pokemon_number in self.newly_acquired
    
    def clear_newly_acquired(self):
        """Clear the newly acquired list (called when viewing outcome)"""
        self.newly_acquired = []
        self.newly_acquired_items = []
    
    def reset_inventory(self):
        """Reset all owned Pokemon and pull statistics (for reset button)"""
        self.pokemon_owned = {}
        self.items_owned = {}
        self.newly_acquired = []
        self.newly_acquired_items = []
        # Reset pull statistics
        self.stats['total_pulls'] = 0
        self.stats['pulls_by_version'] = {'Red': 0, 'Blue': 0, 'Yellow': 0, 'Items': 0}
        # Reset collection complete sound flag
        self.collection_complete_sound_played = False
        print("Inventory and pull statistics reset")
    
    def get_total_owned_count(self) -> int:
        """Get total number of unique Pokemon owned"""
        return len(self.pokemon_owned)
    
    def get_total_pokemon_count(self) -> int:
        """Get total number of Pokemon including duplicates"""
        return sum(self.pokemon_owned.values())
    
    def record_pull(self, version: str, count: int = 1):
        """
        Record gacha pulls for statistics
        
        Args:
            version: "Red", "Blue", or "Yellow"
            count: Number of pulls (1 or 10)
        """
        if 'pulls_by_version' not in self.stats:
            self.stats['pulls_by_version'] = {'Red': 0, 'Blue': 0, 'Yellow': 0}
        
        if version in self.stats['pulls_by_version']:
            self.stats['pulls_by_version'][version] += count
        
        if 'total_pulls' not in self.stats:
            self.stats['total_pulls'] = 0
        self.stats['total_pulls'] += count
    
    def get_total_pulls(self) -> int:
        """Get total number of pulls across all versions"""
        return self.stats.get('total_pulls', 0)
    
    def get_pulls_by_version(self, version: str) -> int:
        """Get number of pulls for a specific version"""
        if 'pulls_by_version' not in self.stats:
            return 0
        return self.stats.get('pulls_by_version', {}).get(version, 0)
    
    # Item Management Methods
    def add_item(self, item_number: str) -> bool:
        """
        Add an item to inventory
        
        Args:
            item_number: Item number (e.g., "001")
            
        Returns:
            True if this is a new item, False if already owned
        """
        is_new = item_number not in self.items_owned
        
        if is_new:
            self.items_owned[item_number] = 1
            self.newly_acquired_items.append(item_number)
        else:
            self.items_owned[item_number] += 1
        
        return is_new
    
    def get_item_count(self, item_number: str) -> int:
        """Get count of owned items"""
        return self.items_owned.get(item_number, 0)
    
    def has_item(self, item_number: str) -> bool:
        """Check if player owns this item"""
        return item_number in self.items_owned
    
    def is_newly_acquired_item(self, item_number: str) -> bool:
        """Check if item is newly acquired (for NEW badge)"""
        return item_number in self.newly_acquired_items
    
    def get_total_items_count(self) -> int:
        """Get total number of unique items owned"""
        return len(self.items_owned)
    
    def get_total_items_quantity(self) -> int:
        """Get total number of items including duplicates"""
        return sum(self.items_owned.values())

