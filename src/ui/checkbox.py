"""
Checkbox UI Component
"""
import pygame
from typing import Callable, Optional


class Checkbox:
    """Interactive checkbox component"""
    
    def __init__(self, x: int, y: int, size: int, label: str,
                 font_manager, font_size: int = 18,
                 checked: bool = False,
                 callback: Optional[Callable[[bool], None]] = None):
        """
        Create a checkbox
        
        Args:
            x, y: Position (top-left of checkbox box)
            size: Size of checkbox box
            label: Label text next to checkbox
            font_manager: FontManager instance
            font_size: Label text size
            checked: Initial checked state
            callback: Function to call when toggled (receives new checked state)
        """
        self.box_rect = pygame.Rect(x, y, size, size)
        self.label = label
        self.font_manager = font_manager
        self.font_size = font_size
        self.checked = checked
        self.callback = callback
        
        # Colors
        self.box_color = (200, 200, 200)
        self.check_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.hover_color = (255, 255, 0)
        
        self.is_hovered = False
        
        # Calculate full clickable area (box + label)
        if font_manager:
            label_width, label_height = font_manager.get_text_size(label, font_size)
            self.click_rect = pygame.Rect(x, y, size + 10 + label_width, max(size, label_height))
        else:
            self.click_rect = self.box_rect.copy()
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse events
        
        Args:
            event: Pygame event
            
        Returns:
            True if checkbox was toggled
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.click_rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.click_rect.collidepoint(event.pos):
                self.checked = not self.checked
                if self.callback:
                    self.callback(self.checked)
                return True
        
        return False
    
    def update(self):
        """Update checkbox state (check hover)"""
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.click_rect.collidepoint(mouse_pos)
    
    def render(self, surface: pygame.Surface):
        """
        Draw the checkbox
        
        Args:
            surface: Surface to draw on
        """
        # Draw checkbox box
        pygame.draw.rect(surface, self.box_color, self.box_rect, 2)
        
        # Draw checkmark if checked
        if self.checked:
            # Draw a checkmark (✓)
            padding = 4
            points = [
                (self.box_rect.left + padding, self.box_rect.centery),
                (self.box_rect.centerx, self.box_rect.bottom - padding),
                (self.box_rect.right - padding, self.box_rect.top + padding)
            ]
            pygame.draw.lines(surface, self.check_color, False, points, 3)
        
        # Draw label
        if self.font_manager:
            text_color = self.hover_color if self.is_hovered else self.text_color
            text_surface = self.font_manager.render_text(self.label, self.font_size, text_color)
            text_x = self.box_rect.right + 10
            text_y = self.box_rect.centery - text_surface.get_height() // 2
            surface.blit(text_surface, (text_x, text_y))
    
    def set_checked(self, checked: bool):
        """Set checked state without calling callback"""
        self.checked = checked
    
    def is_checked(self) -> bool:
        """Get current checked state"""
        return self.checked

