"""
Pokemon Tile UI Component
"""
import pygame
from typing import Optional

class PokemonTile:
    """Displays a Pokemon with image, name, types, and rarity"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 pokemon, resource_manager, font_manager,
                 show_new_badge: bool = False,
                 show_count: bool = False,
                 count: int = 0):
        """
        Initialize Pokemon tile
        
        Args:
            x, y: Top-left position
            width, height: Tile dimensions
            pokemon: Pokemon data object
            resource_manager: ResourceManager instance
            font_manager: FontManager instance
            show_new_badge: Whether to show "NEW!" badge
            show_count: Whether to show owned count
            count: Number owned (if show_count is True)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.pokemon = pokemon
        self.resource_manager = resource_manager
        self.font_manager = font_manager
        self.show_new_badge = show_new_badge
        self.show_count = show_count
        self.count = count
        
        # Get rarity object for colors
        self.rarity_obj = resource_manager.rarities_dict.get(pokemon.rarity)
    
    def render(self, surface: pygame.Surface):
        """Render the Pokemon tile"""
        # Draw background
        bg_color = (40, 40, 50)
        pygame.draw.rect(surface, bg_color, self.rect)
        
        # Draw rarity border
        if self.rarity_obj:
            border_color = self.rarity_obj.get_color_rgb()
            pygame.draw.rect(surface, border_color, self.rect, 3)
        
        # Draw Pokemon image
        image = self.resource_manager.images.get(self.pokemon.image_path)
        if image:
            # Scale to fit (leave room for text)
            img_size = min(self.rect.width - 20, self.rect.height - 60)
            scaled_image = pygame.transform.scale(image, (img_size, img_size))
            img_x = self.rect.x + (self.rect.width - img_size) // 2
            img_y = self.rect.y + 10
            surface.blit(scaled_image, (img_x, img_y))
        
        # Draw Pokemon name (with padding above)
        name_y = self.rect.y + self.rect.height - 40
        if self.font_manager:
            # Use smaller font and truncate name to fit tile width
            font_size = 12
            name = self.pokemon.name
            
            # Check if name fits, truncate if needed
            max_width = self.rect.width - 10  # 5px padding on each side
            while len(name) > 0:
                text_width, _ = self.font_manager.get_text_size(name, font_size)
                if text_width <= max_width:
                    break
                name = name[:-1]
            
            name_surface = self.font_manager.render_text(name, font_size, (255, 255, 255))
            name_rect = name_surface.get_rect(center=(self.rect.centerx, name_y))
            surface.blit(name_surface, name_rect)
        
        # Draw types
        self._render_types(surface)
        
        # Draw "NEW!" badge if applicable
        if self.show_new_badge:
            self._render_new_badge(surface)
        
        # Draw count if applicable
        if self.show_count and self.count > 0:
            self._render_count(surface)
    
    def _render_types(self, surface: pygame.Surface):
        """Render Pokemon type icons/text"""
        types = [self.pokemon.type1]
        if self.pokemon.has_dual_type():
            types.append(self.pokemon.type2)
        
        type_y = self.rect.y + self.rect.height - 25
        
        if len(types) == 1:
            # Single type - centered
            self._render_single_type(surface, types[0], self.rect.centerx, type_y)
        else:
            # Dual type - side by side
            spacing = 35
            start_x = self.rect.centerx - spacing // 2
            self._render_single_type(surface, types[0], start_x, type_y)
            self._render_single_type(surface, types[1], start_x + spacing, type_y)
    
    def _render_single_type(self, surface: pygame.Surface, type_name: str, x: int, y: int):
        """Render a single type icon"""
        type_obj = self.resource_manager.types_dict.get(type_name)
        if not type_obj:
            return
        
        # Get type icon
        icon = self.resource_manager.images.get(type_obj.image_path)
        if icon:
            # Scale icon
            icon_size = 20
            scaled_icon = pygame.transform.scale(icon, (icon_size, icon_size))
            icon_rect = scaled_icon.get_rect(center=(x, y))
            surface.blit(scaled_icon, icon_rect)
    
    def _render_new_badge(self, surface: pygame.Surface):
        """Render "NEW!" badge in top-right corner"""
        if not self.font_manager:
            return
        
        badge_color = (255, 215, 0)  # Gold
        badge_bg = (255, 0, 0)  # Red background
        
        text_surface = self.font_manager.render_text("NEW!", 24, badge_color, is_title=True)
        
        # Background rectangle
        padding = 3
        bg_rect = pygame.Rect(
            self.rect.right - text_surface.get_width() - padding * 2 - 5,
            self.rect.top + 5,
            text_surface.get_width() + padding * 2,
            text_surface.get_height() + padding * 2
        )
        pygame.draw.rect(surface, badge_bg, bg_rect)
        pygame.draw.rect(surface, badge_color, bg_rect, 1)
        
        # Text
        text_x = bg_rect.x + padding
        text_y = bg_rect.y + padding
        surface.blit(text_surface, (text_x, text_y))
    
    def _render_count(self, surface: pygame.Surface):
        """Render owned count in top-left corner"""
        if not self.font_manager or self.count <= 0:
            return
        
        count_text = f"x{self.count}"
        text_surface = self.font_manager.render_text(count_text, 21, (255, 255, 255), is_title=True)
        
        # Background
        padding = 3
        bg_rect = pygame.Rect(
            self.rect.left + 5,
            self.rect.top + 5,
            text_surface.get_width() + padding * 2,
            text_surface.get_height() + padding * 2
        )
        pygame.draw.rect(surface, (0, 0, 0, 180), bg_rect)
        
        # Text
        text_x = bg_rect.x + padding
        text_y = bg_rect.y + padding
        surface.blit(text_surface, (text_x, text_y))

