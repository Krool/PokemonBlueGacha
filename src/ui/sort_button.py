"""
Sort Button UI Component
"""
import pygame
from typing import Callable, Optional
from enum import Enum


class SortOrder(Enum):
    """Sort order enumeration"""
    NONE = 0
    ASCENDING = 1
    DESCENDING = 2


class SortButton:
    """Sort button with three states (none, ascending, descending)"""
    
    def __init__(self, x: int, y: int, width: int, height: int, label: str,
                 font_manager, font_size: int = 20,
                 callback: Optional[Callable[[SortOrder], None]] = None):
        """
        Create a sort button
        
        Args:
            x, y: Position
            width, height: Size
            label: Button text (e.g., "#", "RAR", "CNT")
            font_manager: FontManager instance
            font_size: Text size
            callback: Function to call when clicked (receives new sort order)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.font_manager = font_manager
        self.font_size = font_size
        self.callback = callback
        
        self.sort_order = SortOrder.NONE
        
        # Colors
        self.inactive_color = (80, 80, 80)
        self.active_color = (0, 150, 0)
        self.hover_color = (120, 120, 120)
        self.text_color = (255, 255, 255)
        self.border_color = (255, 255, 255)
        
        self.is_hovered = False
    
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
            if event.button == 1 and self.rect.collidepoint(event.pos):
                # Cycle through states: NONE → ASCENDING → DESCENDING → ASCENDING → ...
                if self.sort_order == SortOrder.NONE:
                    self.sort_order = SortOrder.ASCENDING
                elif self.sort_order == SortOrder.ASCENDING:
                    self.sort_order = SortOrder.DESCENDING
                else:
                    self.sort_order = SortOrder.ASCENDING
                
                if self.callback:
                    self.callback(self.sort_order)
                return True
        
        return False
    
    def update(self):
        """Update button state (check hover)"""
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def render(self, surface: pygame.Surface):
        """
        Draw the sort button
        
        Args:
            surface: Surface to draw on
        """
        # Choose background color
        if self.sort_order != SortOrder.NONE:
            bg_color = self.active_color
        elif self.is_hovered:
            bg_color = self.hover_color
        else:
            bg_color = self.inactive_color
        
        # Draw background
        pygame.draw.rect(surface, bg_color, self.rect)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        
        # Draw label (always centered)
        if self.font_manager:
            label_surface = self.font_manager.render_text(
                self.label, self.font_size, self.text_color
            )
            label_rect = label_surface.get_rect(center=self.rect.center)
            surface.blit(label_surface, label_rect)
            
            # Draw arrow indicator next to label (not centered, fixed position)
            if self.sort_order == SortOrder.ASCENDING:
                arrow_surface = self.font_manager.render_text(
                    "▲", self.font_size - 2, self.text_color
                )
                arrow_rect = arrow_surface.get_rect(
                    centerx=self.rect.centerx,
                    top=label_rect.bottom + 2
                )
                surface.blit(arrow_surface, arrow_rect)
            elif self.sort_order == SortOrder.DESCENDING:
                arrow_surface = self.font_manager.render_text(
                    "▼", self.font_size - 2, self.text_color
                )
                arrow_rect = arrow_surface.get_rect(
                    centerx=self.rect.centerx,
                    top=label_rect.bottom + 2
                )
                surface.blit(arrow_surface, arrow_rect)
    
    def set_sort_order(self, order: SortOrder):
        """Set sort order without calling callback"""
        self.sort_order = order
    
    def get_sort_order(self) -> SortOrder:
        """Get current sort order"""
        return self.sort_order
    
    def reset(self):
        """Reset to NONE state"""
        self.sort_order = SortOrder.NONE

