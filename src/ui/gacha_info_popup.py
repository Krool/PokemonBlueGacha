"""
Gacha Info Popup - Shows all possible Pokemon and their drop rates
"""
import pygame
from config import COLOR_WHITE, COLOR_BLACK, SCREEN_WIDTH, SCREEN_HEIGHT
from ui.button import Button
from typing import Optional, List, Dict


class GachaInfoPopup:
    """Popup displaying all Pokemon drop rates for a gacha machine"""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 machine_name: str,
                 pokemon_list: List,
                 rarities_dict: Dict,
                 font_manager,
                 callback: Optional[callable] = None):
        """
        Initialize gacha info popup
        
        Args:
            x, y: Center position
            width, height: Popup dimensions
            machine_name: Name of the gacha machine (Red, Blue, Yellow)
            pokemon_list: List of all Pokemon
            rarities_dict: Dictionary of rarity data
            font_manager: FontManager instance
            callback: Optional callback when closed
        """
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.font_manager = font_manager
        self.callback = callback
        self.showing = True
        self.machine_name = machine_name
        
        # Calculate drop rates
        self.drop_rates = self._calculate_drop_rates(pokemon_list, rarities_dict, machine_name)
        
        # Scroll state
        self.scroll_offset = 0
        self.max_scroll = 0
        self.content_height = 0
        
        # Content area (leave room for title and close button)
        self.content_rect = pygame.Rect(
            self.rect.left + 20,
            self.rect.top + 80,
            self.rect.width - 40,
            self.rect.height - 160
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
            callback=self.close
        )
    
    def _calculate_drop_rates(self, pokemon_list: List, rarities_dict: Dict, version: str) -> List[tuple]:
        """
        Calculate drop rate for each Pokemon in this version
        
        Returns:
            List of (pokemon, drop_rate_percent) tuples, sorted by drop rate descending
        """
        try:
            # Filter Pokemon available in this version
            available_pokemon = [p for p in pokemon_list if p.get_weight_for_version(version) > 0]
            
            if not available_pokemon:
                print(f"Warning: No Pokemon available for {version}")
                return []
            
            # Calculate total rarity weight
            total_rarity_weight = sum(r.get_weight_for_version(version) for r in rarities_dict.values())
            
            if total_rarity_weight == 0:
                print(f"Warning: Total rarity weight is 0 for {version}")
                return []
            
            rates = []
            
            for pokemon in available_pokemon:
                rarity = rarities_dict.get(pokemon.rarity)
                if not rarity:
                    print(f"Warning: Rarity '{pokemon.rarity}' not found for Pokemon #{pokemon.number}")
                    continue
                
                # Probability of this rarity
                rarity_weight = rarity.get_weight_for_version(version)
                if rarity_weight == 0:
                    continue
                    
                rarity_prob = rarity_weight / total_rarity_weight
                
                # Count Pokemon in same rarity (in this version)
                same_rarity_pokemon = [p for p in available_pokemon if p.rarity == pokemon.rarity]
                total_rarity_pokemon_weight = sum(p.get_weight_for_version(version) 
                                                 for p in same_rarity_pokemon)
                
                if total_rarity_pokemon_weight == 0:
                    continue
                
                # Probability within rarity
                within_rarity_prob = pokemon.get_weight_for_version(version) / total_rarity_pokemon_weight
                
                # Combined probability (as percentage)
                drop_rate_percent = (rarity_prob * within_rarity_prob) * 100
                
                rates.append((pokemon, drop_rate_percent))
            
            # Sort by drop rate descending (rarest first for visual appeal)
            rates.sort(key=lambda x: x[1])
            
            print(f"Calculated {len(rates)} drop rates for {version}")
            return rates
            
        except Exception as e:
            print(f"Error calculating drop rates: {e}")
            import traceback
            traceback.print_exc()
            return []
    
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
        
        # Close on escape or click outside
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
        title_surface = self.font_manager.render_text(f"{self.machine_name.upper()} MACHINE - DROP RATES", 32, COLOR_WHITE, is_title=True)
        title_rect = title_surface.get_rect(center=(self.rect.centerx, self.rect.top + 40))
        surface.blit(title_surface, title_rect)
        
        # Check if we have drop rates to display
        if not self.drop_rates:
            no_data_surface = self.font_manager.render_text("No drop rate data available", 20, COLOR_WHITE)
            no_data_rect = no_data_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
            surface.blit(no_data_surface, no_data_rect)
            self.close_button.render(surface)
            return
        
        # Create a surface for scrollable content
        line_height = 30
        self.content_height = len(self.drop_rates) * line_height
        self.max_scroll = max(0, self.content_height - self.content_rect.height)
        
        # Create clipping surface for scrollable area
        content_surface = pygame.Surface((self.content_rect.width, self.content_rect.height))
        content_surface.fill((40, 40, 40))
        
        # Render Pokemon list
        y = -self.scroll_offset
        for pokemon, drop_rate in self.drop_rates:
            if y + line_height > 0 and y < self.content_rect.height:
                # Pokemon number and name
                name_text = f"#{pokemon.number} {pokemon.name}"
                name_surface = self.font_manager.render_text(name_text, 16, COLOR_WHITE)
                content_surface.blit(name_surface, (10, y))
                
                # Drop rate
                rate_text = f"{drop_rate:.4f}%"
                rate_surface = self.font_manager.render_text(rate_text, 16, (255, 215, 0))
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
                rarity_color = rarity_colors.get(pokemon.rarity, COLOR_WHITE)
                pygame.draw.circle(content_surface, rarity_color, 
                                 (self.content_rect.width // 2 - 50, y + line_height // 2), 6)
            
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

