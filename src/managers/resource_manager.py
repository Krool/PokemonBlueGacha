"""
Resource management for images and assets
"""
import pygame
import os
from typing import Dict, List, Optional
from data.pokemon_data import Pokemon
from data.type_data import PokemonType
from data.rarity_data import Rarity
from data.gacha_machine_data import GachaMachine
from data.item_data import Item


class ResourceManager:
    """Manages loading and caching of game resources"""
    
    def __init__(self):
        # Data storage (loaded by main.py)
        self.pokemon_list: List[Pokemon] = []
        self.types_dict: Dict[str, PokemonType] = {}
        self.rarities_dict: Dict[str, Rarity] = {}
        self.gacha_machines_dict: Dict[str, GachaMachine] = {}
        self.items_list: List[Item] = []
        
        # Image cache
        self.images: Dict[str, pygame.Surface] = {}
        self.placeholder_image: Optional[pygame.Surface] = None
        
        # Special images
        self.gacha_item_image: Optional[pygame.Surface] = None
        
        self._create_placeholder()
    
    def _create_placeholder(self):
        """Create a placeholder image for missing assets"""
        self.placeholder_image = pygame.Surface((64, 64))
        self.placeholder_image.fill((255, 0, 255))  # Magenta placeholder
        
        # Draw an X
        pygame.draw.line(self.placeholder_image, (0, 0, 0), (0, 0), (64, 64), 2)
        pygame.draw.line(self.placeholder_image, (0, 0, 0), (64, 0), (0, 64), 2)
    
    def load_image(self, path: str, convert_alpha: bool = True) -> pygame.Surface:
        """
        Load and cache an image
        
        Args:
            path: Path to image file (relative to project root)
            convert_alpha: Whether to convert with alpha channel
            
        Returns:
            Loaded pygame Surface, or placeholder if not found
        """
        # Check cache first
        if path in self.images:
            return self.images[path]
        
        # Try to load
        if not os.path.exists(path):
            print(f"Warning: Image not found: {path}")
            return self.placeholder_image
        
        try:
            image = pygame.image.load(path)
            if convert_alpha:
                image = image.convert_alpha()
            else:
                image = image.convert()
            
            self.images[path] = image
            return image
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return self.placeholder_image
    
    def get_pokemon_sprite(self, pokemon_number: str) -> pygame.Surface:
        """
        Get Pokemon sprite by number
        
        Args:
            pokemon_number: Pokemon number (e.g., "001")
            
        Returns:
            Pokemon sprite Surface
        """
        # Find Pokemon in list
        for pokemon in self.pokemon_list:
            if pokemon.number == pokemon_number:
                return self.load_image(pokemon.image_path)
        
        print(f"Warning: Pokemon {pokemon_number} not found")
        return self.placeholder_image
    
    def get_type_icon(self, type_name: str) -> pygame.Surface:
        """
        Get type icon by name
        
        Args:
            type_name: Type name (e.g., "Fire")
            
        Returns:
            Type icon Surface
        """
        if type_name in self.types_dict:
            return self.load_image(self.types_dict[type_name].image_path)
        
        print(f"Warning: Type {type_name} not found")
        return self.placeholder_image
    
    def get_pokemon_by_number(self, pokemon_number: str) -> Optional[Pokemon]:
        """Get Pokemon data object by number"""
        for pokemon in self.pokemon_list:
            if pokemon.number == pokemon_number:
                return pokemon
        return None
    
    def get_type(self, type_name: str) -> Optional[PokemonType]:
        """Get type data object by name"""
        return self.types_dict.get(type_name)
    
    def get_rarity(self, rarity_name: str) -> Optional[Rarity]:
        """Get rarity data object by name"""
        return self.rarities_dict.get(rarity_name)
    
    def get_gacha_machine(self, version: str) -> Optional[GachaMachine]:
        """Get gacha machine data object by version name"""
        return self.gacha_machines_dict.get(version)
    
    def get_item_by_number(self, item_number: str) -> Optional[Item]:
        """Get Item data object by number"""
        for item in self.items_list:
            if item.number == item_number:
                return item
        return None
    
    def get_item_icon(self, item_number: str) -> pygame.Surface:
        """
        Get item icon by number
        
        Args:
            item_number: Item number (e.g., "001")
            
        Returns:
            Item icon Surface
        """
        item = self.get_item_by_number(item_number)
        if item:
            return self.load_image(item.get_icon_path())
        
        print(f"Warning: Item {item_number} not found")
        return self.placeholder_image
    
    def preload_all_sprites(self, progress_callback=None):
        """
        Preload all Pokemon and type sprites (call during loading screen)
        
        Args:
            progress_callback: Optional callback function(current, total) for progress updates
        """
        print("Preloading sprites...")
        
        total_images = len(self.pokemon_list) + len(self.types_dict)
        current = 0
        
        # Load all Pokemon sprites
        for pokemon in self.pokemon_list:
            self.load_image(pokemon.image_path)
            current += 1
            if progress_callback:
                progress_callback(current, total_images)
        
        # Load all type icons
        for type_name, poke_type in self.types_dict.items():
            self.load_image(poke_type.image_path)
            current += 1
            if progress_callback:
                progress_callback(current, total_images)
        
        print(f"✓ Preloaded {len(self.images)} images")
    
    def load_ui_images(self, logo_path: str, gacha_red_path: str, 
                       gacha_blue_path: str, gacha_yellow_path: str, gacha_item_path: str,
                       pokedollar_icon_path: str, rays_path: str):
        """
        Load UI images (logo, gacha machines, currency icon, rays effect)
        
        Args:
            logo_path: Path to logo image
            gacha_red_path: Path to red gacha machine image
            gacha_blue_path: Path to blue gacha machine image
            gacha_yellow_path: Path to yellow gacha machine image
            gacha_item_path: Path to items gacha machine image
            pokedollar_icon_path: Path to Pokédollar icon image
            rays_path: Path to rays background effect image
        """
        self.logo = self.load_image(logo_path)
        self.gacha_red = self.load_image(gacha_red_path)
        self.gacha_blue = self.load_image(gacha_blue_path)
        self.gacha_yellow = self.load_image(gacha_yellow_path)
        self.gacha_item = self.load_image(gacha_item_path)
        self.pokedollar_icon = self.load_image(pokedollar_icon_path)
        self.rays = self.load_image(rays_path)
        print("✓ UI images loaded")

