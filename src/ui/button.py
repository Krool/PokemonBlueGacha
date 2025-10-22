"""
Button UI component
"""
import pygame
from typing import Callable, Optional


class Button:
    """Interactive button component"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 font_manager, font_size: int = 24,
                 bg_color: tuple = (100, 100, 100),
                 hover_color: tuple = (150, 150, 150),
                 text_color: tuple = (255, 255, 255),
                 border_color: tuple = (255, 255, 255),
                 border_width: int = 2,
                 use_title_font: bool = False,
                 callback: Optional[Callable] = None,
                 audio_manager = None,
                 play_click_sound: bool = True):
        """
        Create a button
        
        Args:
            x, y: Position
            width, height: Size
            text: Button text
            font_manager: FontManager instance
            font_size: Text size
            bg_color: Background color
            hover_color: Color when hovering
            text_color: Text color
            border_color: Border color
            border_width: Border thickness
            use_title_font: Whether to use title font for button text
            callback: Function to call when clicked
            audio_manager: AudioManager instance for click sounds (optional)
            play_click_sound: Whether to play click sound when pressed (default True)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_manager = font_manager
        self.font_size = font_size
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.use_title_font = use_title_font
        self.callback = callback
        self.audio_manager = audio_manager
        self.play_click_sound = play_click_sound
        
        self.is_hovered = False
        self.is_pressed = False
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse events
        
        Args:
            event: Pygame event
            
        Returns:
            True if button was clicked
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed and self.is_hovered:
                self.is_pressed = False
                # Play click sound (if enabled)
                if self.audio_manager and self.play_click_sound:
                    self.audio_manager.play_random_click_sound()
                if self.callback:
                    self.callback()
                return True
            self.is_pressed = False
        
        return False
    
    def update(self):
        """Update button state (check hover)"""
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def render(self, surface: pygame.Surface):
        """
        Draw the button
        
        Args:
            surface: Surface to draw on
        """
        # Choose color based on state
        color = self.hover_color if self.is_hovered else self.bg_color
        
        # Draw background
        pygame.draw.rect(surface, color, self.rect)
        
        # Draw border
        if self.border_width > 0:
            pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)
        
        # Draw text
        text_surface, text_pos = self.font_manager.render_text_centered(
            self.text, self.font_size, self.text_color, self.rect, is_title=self.use_title_font
        )
        surface.blit(text_surface, text_pos)
    
    def set_text(self, text: str):
        """Update button text"""
        self.text = text
    
    def set_position(self, x: int, y: int):
        """Update button position"""
        self.rect.x = x
        self.rect.y = y
    
    def set_enabled(self, enabled: bool):
        """Enable/disable the button (visual feedback)"""
        if not enabled:
            self.bg_color = (80, 80, 80)
            self.hover_color = (80, 80, 80)
        # You might want to store original colors to restore

