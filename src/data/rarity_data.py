"""
Rarity data structure
"""
from dataclasses import dataclass


@dataclass
class Rarity:
    """Represents a rarity tier"""
    name: str           # "Legendary"
    red_weight: int     # 1
    blue_weight: int    # 1
    yellow_weight: int  # 2 (for Legendary in Yellow)
    items_weight: int   # 1 (for Items gacha)
    color_hex: str      # "#FF8000"
    
    def get_color_rgb(self) -> tuple:
        """Convert hex to RGB tuple (r, g, b)"""
        hex_color = self.color_hex.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def get_weight_for_version(self, version: str) -> int:
        """Get drop weight for specific version (Red, Blue, Yellow, or Items)"""
        if version == "Red":
            return self.red_weight
        elif version == "Blue":
            return self.blue_weight
        elif version == "Yellow":
            return self.yellow_weight
        elif version == "Items":
            return self.items_weight
        else:
            return 0

