"""
Type data structure
"""
from dataclasses import dataclass


@dataclass
class PokemonType:
    """Represents a Pokémon type"""
    name: str        # "Fire"
    image_path: str  # "Assets/Sprites/Types/Fire.png"
    color_hex: str   # "#F08030"
    
    def get_color_rgb(self) -> tuple:
        """Convert hex to RGB tuple (r, g, b)"""
        hex_color = self.color_hex.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

