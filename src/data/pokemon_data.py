"""
Pokemon data structure
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Pokemon:
    """Represents a single Pokémon"""
    number: str          # "001"
    name: str            # "Bulbasaur"
    type1: str           # "Grass"
    type2: Optional[str] # "Poison" or None
    rarity: str          # "Uncommon"
    red_weight: int      # 1 (0 if exclusive to other versions)
    blue_weight: int     # 1 (0 if exclusive to other versions)
    yellow_weight: int   # 1 (0 if exclusive to other versions)
    image_path: str      # "Assets/Sprites/Pokemon/001_Bulbasaur.png"
    
    def get_pokedex_num(self) -> int:
        """Returns numeric Pokédex number"""
        return int(self.number)
    
    def has_dual_type(self) -> bool:
        """Check if Pokémon has two types"""
        return self.type2 is not None and self.type2 != ""
    
    def get_weight_for_version(self, version: str) -> int:
        """Get drop weight for specific version (Red, Blue, or Yellow)"""
        if version == "Red":
            return self.red_weight
        elif version == "Blue":
            return self.blue_weight
        elif version == "Yellow":
            return self.yellow_weight
        else:
            return 0

