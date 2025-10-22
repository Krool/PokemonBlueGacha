"""
Item Tile Component - Displays a single item with icon, name, rarity, and optional badges
"""
import pygame
from config import COLOR_WHITE, COLOR_BLACK


class ItemTile:
    """Visual component for displaying an item"""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 item, resource_manager, font_manager,
                 show_new_badge: bool = False,
                 show_count: bool = False,
                 count: int = 0):
        """
        Initialize item tile
        
        Args:
            x, y: Position
            width, height: Dimensions
            item: Item object
            resource_manager: ResourceManager instance
            font_manager: FontManager instance
            show_new_badge: Whether to show NEW! badge
            show_count: Whether to show count
            count: Item count to display
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.item = item
        self.resource_manager = resource_manager
        self.font_manager = font_manager
        self.show_new_badge = show_new_badge
        self.show_count = show_count
        self.count = count
    
    def render(self, surface: pygame.Surface):
        """Render the item tile"""
        # Get rarity color
        rarity_obj = self.resource_manager.rarities_dict.get(self.item.rarity)
        rarity_color = rarity_obj.get_color_rgb() if rarity_obj else COLOR_WHITE
        
        # Draw background
        pygame.draw.rect(surface, COLOR_BLACK, self.rect)
        
        # Draw rarity-colored border
        border_width = 4
        pygame.draw.rect(surface, rarity_color, self.rect, border_width)
        
        # Draw item icon
        icon = self.resource_manager.get_item_icon(self.item.number)
        if icon:
            # Scale icon to fit nicely (leave space for name)
            icon_size = min(self.rect.width - 40, self.rect.height - 80)
            scaled_icon = pygame.transform.scale(icon, (icon_size, icon_size))
            
            icon_x = self.rect.centerx - icon_size // 2
            icon_y = self.rect.top + 20
            surface.blit(scaled_icon, (icon_x, icon_y))
        
        # Draw item name
        if self.font_manager:
            # Truncate name if too long
            name = self.item.name
            max_length = 15
            if len(name) > max_length:
                name = name[:max_length - 2] + ".."
            
            name_size = 18 if self.rect.width > 200 else 14
            name_surface = self.font_manager.render_text(name, name_size, COLOR_WHITE)
            name_rect = name_surface.get_rect(center=(self.rect.centerx, self.rect.bottom - 40))
            surface.blit(name_surface, name_rect)
            
            # Draw value below name
            value_text = f"{self.item.value:,} ₽"
            value_surface = self.font_manager.render_text(value_text, 14, (255, 215, 0))
            value_rect = value_surface.get_rect(center=(self.rect.centerx, self.rect.bottom - 20))
            surface.blit(value_surface, value_rect)
        
        # Draw NEW! badge
        if self.show_new_badge:
            badge_width = 80
            badge_height = 30
            badge_x = self.rect.right - badge_width - 5
            badge_y = self.rect.top + 5
            badge_rect = pygame.Rect(badge_x, badge_y, badge_width, badge_height)
            
            # Draw yellow background
            pygame.draw.rect(surface, (255, 255, 0), badge_rect)
            pygame.draw.rect(surface, (200, 200, 0), badge_rect, 2)
            
            # Draw NEW! text
            if self.font_manager:
                new_text = self.font_manager.render_text("NEW!", 20, COLOR_BLACK, is_title=True)
                new_rect = new_text.get_rect(center=badge_rect.center)
                surface.blit(new_text, new_rect)
        
        # Draw count
        if self.show_count and self.count > 0:
            count_text = f"x{self.count}"
            if self.font_manager:
                count_surface = self.font_manager.render_text(count_text, 24, COLOR_WHITE, is_title=True)
                count_rect = count_surface.get_rect()
                count_rect.bottomleft = (self.rect.left + 8, self.rect.bottom - 5)
                
                # Draw semi-transparent background
                bg_rect = count_rect.inflate(8, 4)
                bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                bg_surface.fill((0, 0, 0, 180))
                surface.blit(bg_surface, bg_rect.topleft)
                
                surface.blit(count_surface, count_rect)

