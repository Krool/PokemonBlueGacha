"""
Items Info Popup - Shows all possible items and their drop rates
"""
import pygame
from config import COLOR_WHITE, COLOR_BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, IS_WEB
from ui.button import Button
from typing import Optional, List, Dict
from logic.items_gacha import calculate_item_drop_rate, calculate_expected_value


class ItemsInfoPopup:
    """Popup displaying all item drop rates for the Items gacha"""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 items_list: List,
                 rarities_dict: Dict,
                 font_manager,
                 callback: Optional[callable] = None,
                 audio_manager = None):
        """
        Initialize items info popup
        
        Args:
            x, y: Center position
            width, height: Popup dimensions
            items_list: List of all Item objects
            rarities_dict: Dictionary of rarity data
            font_manager: FontManager instance
            callback: Optional callback when closed
            audio_manager: AudioManager instance for click sounds (optional)
        """
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.font_manager = font_manager
        self.callback = callback
        self.showing = True
        self.audio_manager = audio_manager
        
        # Calculate drop rates and expected value
        self.drop_rates = self._calculate_drop_rates(items_list, rarities_dict)
        self.expected_value = calculate_expected_value(items_list, rarities_dict)
        
        # Scroll state
        self.scroll_offset = 0
        self.max_scroll = 0
        self.content_height = 0
        
        # Content area (leave room for title, expected value, and close button)
        self.content_rect = pygame.Rect(
            self.rect.left + 20,
            self.rect.top + 140,
            self.rect.width - 40,
            self.rect.height - 220
        )
        
        # Close button
        button_width = 150
        button_height = 50
        self.close_button = Button(
            self.rect.centerx - button_width // 2,
            self.rect.bottom - button_height - 20,
            button_width,
            button_height,
            "CLOSE",
            font_manager,
            font_size=22,
            use_title_font=True,
            bg_color=(100, 100, 100),
            hover_color=(150, 150, 150),
            callback=self.close,
            audio_manager=audio_manager
        )
    
    def _calculate_drop_rates(self, items_list: List, rarities_dict: Dict) -> List[tuple]:
        """
        Calculate drop rate for each item
        
        Returns:
            List of (item, drop_rate_percent) tuples, sorted by drop rate ascending
        """
        rates = []
        
        for item in items_list:
            drop_rate = calculate_item_drop_rate(item, items_list, rarities_dict)
            rates.append((item, drop_rate))
        
        # Sort by drop rate ascending (rarest first for visual appeal)
        rates.sort(key=lambda x: x[1])
        
        return rates
    
    def close(self):
        """Close the popup"""
        self.showing = False
        if self.callback:
            self.callback()
    
    def is_showing(self) -> bool:
        """Check if popup is visible"""
        return self.showing
    
    def handle_event(self, event: pygame.event.Event):
        """Handle input events"""
        if not self.showing:
            return
        
        self.close_button.handle_event(event)
        
        # Handle scrolling
        if event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                # Scroll up/down
                self.scroll_offset -= event.y * 30  # 30 pixels per scroll
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
        
        # Close on escape (desktop only) or click outside
        if not IS_WEB and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.close()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not self.rect.collidepoint(event.pos):
                self.close()
    
    def update(self):
        """Update popup state"""
        if not self.showing:
            return
        
        self.close_button.update()
    
    def render(self, surface: pygame.Surface):
        """Render the popup"""
        if not self.showing:
            return
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Draw popup background
        pygame.draw.rect(surface, (40, 40, 40), self.rect)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 3)
        
        if not self.font_manager:
            return
        
        # Title
        title_surface = self.font_manager.render_text("ITEMS MACHINE - DROP RATES", 32, COLOR_WHITE, is_title=True)
        title_rect = title_surface.get_rect(center=(self.rect.centerx, self.rect.top + 40))
        surface.blit(title_surface, title_rect)
        
        # Expected value
        expected_text = f"Expected Value: ~{int(self.expected_value):,} Pokédollars per pull"
        expected_surface = self.font_manager.render_text(expected_text, 18, (255, 215, 0))
        expected_rect = expected_surface.get_rect(center=(self.rect.centerx, self.rect.top + 80))
        surface.blit(expected_surface, expected_rect)
        
        # Cost comparison
        cost_text = "1-Pull: 800 | 10-Pull: 7,200 (720 each)"
        cost_surface = self.font_manager.render_text(cost_text, 16, (200, 200, 200))
        cost_rect = cost_surface.get_rect(center=(self.rect.centerx, self.rect.top + 105))
        surface.blit(cost_surface, cost_rect)
        
        # Check if we have drop rates to display
        if not self.drop_rates:
            no_data_surface = self.font_manager.render_text("No drop rate data available", 20, COLOR_WHITE)
            no_data_rect = no_data_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
            surface.blit(no_data_surface, no_data_rect)
            self.close_button.render(surface)
            return
        
        # Create a surface for scrollable content
        line_height = 28
        self.content_height = len(self.drop_rates) * line_height
        self.max_scroll = max(0, self.content_height - self.content_rect.height)
        
        # Create clipping surface for scrollable area
        content_surface = pygame.Surface((self.content_rect.width, self.content_rect.height))
        content_surface.fill((40, 40, 40))
        
        # Render items list
        y = -self.scroll_offset
        for item, drop_rate in self.drop_rates:
            if y + line_height > 0 and y < self.content_rect.height:
                # Item number and name
                name_text = f"#{item.number} {item.name}"
                name_surface = self.font_manager.render_text(name_text, 15, COLOR_WHITE)
                content_surface.blit(name_surface, (10, y))
                
                # Drop rate
                rate_text = f"{drop_rate:.4f}%"
                rate_surface = self.font_manager.render_text(rate_text, 15, (255, 215, 0))
                rate_rect = rate_surface.get_rect(right=self.content_rect.width - 10, top=y)
                content_surface.blit(rate_surface, rate_rect)
                
                # Rarity indicator (colored dot)
                rarity_colors = {
                    "Common": (255, 255, 255),
                    "Uncommon": (30, 255, 0),
                    "Rare": (0, 112, 221),
                    "Epic": (163, 53, 238),
                    "Legendary": (255, 128, 0)
                }
                rarity_color = rarity_colors.get(item.rarity, COLOR_WHITE)
                pygame.draw.circle(content_surface, rarity_color, 
                                 (self.content_rect.width // 2 - 30, y + line_height // 2), 5)
            
            y += line_height
        
        # Draw content surface with clipping
        surface.blit(content_surface, self.content_rect.topleft)
        
        # Draw scrollbar if needed
        if self.max_scroll > 0:
            scrollbar_height = max(30, int(self.content_rect.height * (self.content_rect.height / self.content_height)))
            scrollbar_y = self.content_rect.top + int((self.scroll_offset / self.max_scroll) * (self.content_rect.height - scrollbar_height))
            scrollbar_rect = pygame.Rect(self.rect.right - 15, scrollbar_y, 8, scrollbar_height)
            pygame.draw.rect(surface, (150, 150, 150), scrollbar_rect)
        
        # Close button
        self.close_button.render(surface)

