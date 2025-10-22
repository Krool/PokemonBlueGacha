"""
Pokemon Details Popup UI Component
Displays detailed information about a Pokemon
"""
import pygame
from typing import Optional
from config import SCREEN_WIDTH, SCREEN_HEIGHT, IS_WEB

# Colors
COLOR_OVERLAY = (0, 0, 0, 180)  # Semi-transparent black overlay
COLOR_POPUP_BG = (30, 30, 40)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (150, 150, 150)
COLOR_SEPARATOR = (100, 100, 110)


class PokemonDetailsPopup:
    """Displays detailed Pokemon information in a popup"""
    
    def __init__(self, screen, font_manager, resource_manager):
        """
        Initialize Pokemon details popup
        
        Args:
            screen: Pygame screen surface
            font_manager: FontManager instance
            resource_manager: ResourceManager instance
        """
        self.screen = screen
        self.font_manager = font_manager
        self.resource_manager = resource_manager
        self.pokemon = None
        self.showing = False
        
        # Popup dimensions
        self.popup_width = 750
        self.popup_height = 500
        self.popup_x = (SCREEN_WIDTH - self.popup_width) // 2
        self.popup_y = (SCREEN_HEIGHT - self.popup_height) // 2
        self.popup_rect = pygame.Rect(self.popup_x, self.popup_y, self.popup_width, self.popup_height)
        
    def show(self, pokemon):
        """Show the popup with the given Pokemon"""
        self.pokemon = pokemon
        self.showing = True
        
    def hide(self):
        """Hide the popup"""
        self.showing = False
        self.pokemon = None
        
    def is_showing(self) -> bool:
        """Check if popup is currently showing"""
        return self.showing
        
    def handle_event(self, event) -> bool:
        """
        Handle input events
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled, False otherwise
        """
        if not self.showing:
            return False
            
        # Close on click anywhere
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.hide()
            return True
            
        # Close on ESC key (desktop only)
        if not IS_WEB and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.hide()
            return True
            
        return False
        
    def render(self, surface: pygame.Surface):
        """Render the popup"""
        if not self.showing or not self.pokemon:
            return
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        surface.blit(overlay, (0, 0))
        
        # Draw popup background
        pygame.draw.rect(surface, COLOR_POPUP_BG, self.popup_rect)
        
        # Draw border based on rarity
        rarity_obj = self.resource_manager.rarities_dict.get(self.pokemon.rarity)
        if rarity_obj:
            border_color = rarity_obj.get_color_rgb()
            pygame.draw.rect(surface, border_color, self.popup_rect, 4)
        
        # Render content
        self._render_content(surface)
        
    def _render_content(self, surface: pygame.Surface):
        """Render the popup content"""
        padding = 40
        content_x = self.popup_x + padding
        content_y = self.popup_y + padding
        
        # Column 1: Pokemon image and number
        col1_x = content_x
        col1_width = 200
        
        # Column 2: Pokemon info
        col2_x = content_x + col1_width + 40
        col2_width = self.popup_width - col1_width - padding * 2 - 40
        
        # Draw Pokemon image (column 1, top)
        image = self.resource_manager.images.get(self.pokemon.image_path)
        if image:
            img_size = 150
            scaled_image = pygame.transform.scale(image, (img_size, img_size))
            img_x = col1_x + (col1_width - img_size) // 2
            surface.blit(scaled_image, (img_x, content_y))
        
        # Draw Pokemon number (column 1, bottom)
        number_text = f"No. {self.pokemon.number}"
        number_surface = self.font_manager.render_text(number_text, 28, COLOR_WHITE, is_title=True)
        number_y = content_y + 160
        number_x = col1_x + (col1_width - number_surface.get_width()) // 2
        surface.blit(number_surface, (number_x, number_y))
        
        # Draw Pokemon name (column 2, top)
        name_surface = self.font_manager.render_text(self.pokemon.name, 36, COLOR_WHITE, is_title=True)
        surface.blit(name_surface, (col2_x, content_y))
        
        # Draw species (column 2) - right aligned values
        species_y = content_y + 50
        species_label = self.font_manager.render_text("Species:", 18, COLOR_GRAY)
        species_value = self.font_manager.render_text(self.pokemon.species, 18, COLOR_WHITE)
        surface.blit(species_label, (col2_x, species_y))
        # Right align the value at the right edge of column 2
        value_x = col2_x + col2_width - species_value.get_width()
        surface.blit(species_value, (value_x, species_y))
        
        # Draw height (column 2) - right aligned values
        height_y = species_y + 30
        height_label = self.font_manager.render_text("Height:", 18, COLOR_GRAY)
        height_value = self.font_manager.render_text(f"{self.pokemon.height_ft}'", 18, COLOR_WHITE)
        surface.blit(height_label, (col2_x, height_y))
        # Right align the value
        value_x = col2_x + col2_width - height_value.get_width()
        surface.blit(height_value, (value_x, height_y))
        
        # Draw weight (column 2) - right aligned values
        weight_y = height_y + 30
        weight_label = self.font_manager.render_text("Weight:", 18, COLOR_GRAY)
        weight_value = self.font_manager.render_text(f"{self.pokemon.weight_lbs} lbs", 18, COLOR_WHITE)
        surface.blit(weight_label, (col2_x, weight_y))
        # Right align the value
        value_x = col2_x + col2_width - weight_value.get_width()
        surface.blit(weight_value, (value_x, weight_y))
        
        # Draw separator line
        separator_y = content_y + 220
        pygame.draw.line(surface, COLOR_SEPARATOR, 
                        (self.popup_x + padding, separator_y), 
                        (self.popup_x + self.popup_width - padding, separator_y), 
                        2)
        
        # Draw Pokedex entry (below separator, full width)
        entry_y = separator_y + 30
        entry_x = self.popup_x + padding
        entry_width = self.popup_width - padding * 2
        
        # Wrap text to fit
        wrapped_lines = self._wrap_text(self.pokemon.pokedex_entry, entry_width, 18)
        
        for i, line in enumerate(wrapped_lines):
            line_surface = self.font_manager.render_text(line, 18, COLOR_WHITE)
            surface.blit(line_surface, (entry_x, entry_y + i * 25))
        
        # Draw "Tap anywhere to close" hint at bottom
        hint_text = "Tap anywhere to close"
        hint_surface = self.font_manager.render_text(hint_text, 14, COLOR_GRAY)
        hint_x = self.popup_x + (self.popup_width - hint_surface.get_width()) // 2
        hint_y = self.popup_y + self.popup_height - 30
        surface.blit(hint_surface, (hint_x, hint_y))
        
    def _wrap_text(self, text: str, max_width: int, font_size: int) -> list:
        """
        Wrap text to fit within max_width
        
        Args:
            text: Text to wrap
            max_width: Maximum width in pixels
            font_size: Font size to use
            
        Returns:
            List of wrapped lines
        """
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            width, _ = self.font_manager.get_text_size(test_line, font_size)
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Single word is too long, just add it
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

