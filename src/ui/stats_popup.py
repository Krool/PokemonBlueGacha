"""
Statistics popup UI component
"""
import pygame
from config import COLOR_WHITE, COLOR_BLACK, SCREEN_WIDTH, SCREEN_HEIGHT
from ui.button import Button
from typing import Optional


class StatsPopup:
    """Popup displaying gacha statistics"""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 total_pulls: int,
                 red_pulls: int, red_expected: float,
                 blue_pulls: int, blue_expected: float,
                 yellow_pulls: int, yellow_expected: float,
                 total_expected_from_scratch: float,
                 optimal_cost: int,
                 font_manager,
                 game_data=None,
                 callback: Optional[callable] = None,
                 audio_manager = None):
        """
        Initialize stats popup
        
        Args:
            x, y: Center position
            width, height: Popup dimensions
            total_pulls: Total pulls across all versions
            red_pulls: Pulls from Red machine
            red_expected: Expected pulls to get rarest remaining Red Pokemon
            blue_pulls: Pulls from Blue machine
            blue_expected: Expected pulls to get rarest remaining Blue Pokemon
            yellow_pulls: Pulls from Yellow machine
            yellow_expected: Expected pulls to get rarest remaining Yellow Pokemon
            total_expected_from_scratch: Total expected pulls from scratch (sum)
            optimal_cost: Expected Pokédollar cost using optimal strategy
            font_manager: FontManager instance
            callback: Optional callback when closed
            audio_manager: AudioManager instance for click sounds (optional)
        """
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.font_manager = font_manager
        self.callback = callback
        self.showing = True
        self.audio_manager = audio_manager
        
        # Stats data
        self.total_pulls = total_pulls
        self.red_pulls = red_pulls
        self.red_expected = red_expected
        self.blue_pulls = blue_pulls
        self.blue_expected = blue_expected
        self.yellow_pulls = yellow_pulls
        self.yellow_expected = yellow_expected
        self.total_expected_from_scratch = total_expected_from_scratch
        self.optimal_cost = optimal_cost
        self.game_data = game_data
        
        # Clickable area for optimal cost (will be set during render)
        self.optimal_cost_rect = None
        
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
        
        # Check for click on optimal cost
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.optimal_cost_rect and self.optimal_cost_rect.collidepoint(event.pos):
                if self.game_data:
                    self.game_data.gold = self.optimal_cost
                    self.game_data.save()
                    print(f"Set gold to optimal strategy cost: {self.optimal_cost:,}")
                return  # Don't close popup or process other events
        
        # Also close on escape or click outside
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
        title_surface = self.font_manager.render_text("GACHA STATISTICS", 32, COLOR_WHITE, is_title=True)
        title_rect = title_surface.get_rect(center=(self.rect.centerx, self.rect.top + 40))
        surface.blit(title_surface, title_rect)
        
        # Stats content
        y_offset = self.rect.top + 90
        line_height = 30
        
        # Total pulls
        self._render_line(surface, f"Total Pulls Done: {self.total_pulls:,}", y_offset, 24, COLOR_WHITE, is_title=True)
        y_offset += line_height + 10
        
        # Separator
        pygame.draw.line(surface, (100, 100, 100), 
                        (self.rect.left + 40, y_offset), 
                        (self.rect.right - 40, y_offset), 2)
        y_offset += 20
        
        # Section: Pulls by Version
        self._render_line(surface, "Pulls by Version:", y_offset, 20, (255, 255, 100))
        y_offset += line_height
        
        self._render_line(surface, f"  Red:    {self.red_pulls:>4,} pulls", y_offset, 18, COLOR_WHITE)
        y_offset += line_height
        
        self._render_line(surface, f"  Blue:   {self.blue_pulls:>4,} pulls", y_offset, 18, COLOR_WHITE)
        y_offset += line_height
        
        self._render_line(surface, f"  Yellow: {self.yellow_pulls:>4,} pulls", y_offset, 18, COLOR_WHITE)
        y_offset += line_height + 10
        
        # Separator
        pygame.draw.line(surface, (100, 100, 100), 
                        (self.rect.left + 40, y_offset), 
                        (self.rect.right - 40, y_offset), 2)
        y_offset += 20
        
        # Section: Expected Remaining Pulls
        self._render_line(surface, "Expected Pulls (Rarest Pokemon):", y_offset, 20, (255, 255, 100))
        y_offset += line_height
        
        self._render_line(surface, f"  Red:    ~{int(self.red_expected):,} pulls", y_offset, 18, COLOR_WHITE)
        y_offset += line_height
        
        self._render_line(surface, f"  Blue:   ~{int(self.blue_expected):,} pulls", y_offset, 18, COLOR_WHITE)
        y_offset += line_height
        
        self._render_line(surface, f"  Yellow: ~{int(self.yellow_expected):,} pulls", y_offset, 18, COLOR_WHITE)
        y_offset += line_height + 10
        
        # Separator
        pygame.draw.line(surface, (100, 100, 100), 
                        (self.rect.left + 40, y_offset), 
                        (self.rect.right - 40, y_offset), 2)
        y_offset += 20
        
        # Expected from scratch (show sum)
        self._render_line(surface, "Expected From Scratch:", 
                         y_offset, 20, (255, 255, 100))
        y_offset += line_height
        
        self._render_line(surface, f"~{int(self.total_expected_from_scratch):,} pulls", 
                         y_offset, 22, (100, 255, 100), is_title=True)
        y_offset += line_height + 10
        
        # Separator
        pygame.draw.line(surface, (100, 100, 100), 
                        (self.rect.left + 40, y_offset), 
                        (self.rect.right - 40, y_offset), 2)
        y_offset += 20
        
        # Optimal strategy cost (clickable)
        self._render_line(surface, "Optimal Strategy Cost:", 
                         y_offset, 20, (255, 255, 100))
        y_offset += line_height - 5
        
        # Render the cost and store its rect for clicking
        cost_text = f"~{self.optimal_cost:,}"
        cost_surface = self.font_manager.render_text(cost_text, 24, (255, 215, 0), is_title=True)
        cost_rect = cost_surface.get_rect(center=(self.rect.centerx, y_offset))
        surface.blit(cost_surface, cost_rect)
        
        # Store rect for click detection (make it slightly larger for easier clicking)
        self.optimal_cost_rect = cost_rect.inflate(20, 10)
        
        y_offset += line_height - 5
        
        self._render_line(surface, "(Yellow first then Red/Blue for exclusives)", 
                         y_offset, 13, (180, 180, 180))
        
        # Close button
        self.close_button.render(surface)
    
    def _render_line(self, surface: pygame.Surface, text: str, y: int, 
                     font_size: int, color: tuple, is_title: bool = False):
        """Helper to render a centered line of text"""
        text_surface = self.font_manager.render_text(text, font_size, color, is_title=is_title)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, y))
        surface.blit(text_surface, text_rect)

