"""
Item data structure
"""

class Item:
    """Represents a game item"""
    
    def __init__(self, number: str, name: str, index: int, category: str, 
                 value: int, rarity: str, weight: int, icon: str):
        """
        Initialize Item
        
        Args:
            number: Item number (1-79)
            name: Item name
            index: Gen 1 index number
            category: Item category (ball, medicine, etc.)
            value: Item value in Pokédollars
            rarity: Rarity tier
            weight: Drop weight
            icon: Icon filename
        """
        self.number = str(number).zfill(3)  # e.g., "001"
        self.name = name
        self.index = index
        self.category = category
        self.value = value
        self.rarity = rarity
        self.weight = weight
        self.icon = icon
    
    def __repr__(self):
        return f"Item({self.number}, {self.name}, {self.rarity})"
    
    def get_icon_path(self) -> str:
        """Get full path to item icon"""
        return f"Assets/Sprites/Items/{self.icon.split('/')[-1]}"

