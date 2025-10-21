"""
Popup/Modal UI Component
"""
import pygame
from typing import Callable, Optional
from ui.currency_display import CurrencyDisplay


class Popup:
    """Modal popup dialog box"""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 title: str, message: str, font_manager,
                 button_text: str = "OK",
                 callback: Optional[Callable] = None,
                 add_gold_callback: Optional[Callable] = None,
                 pokedollar_icon: Optional[pygame.Surface] = None):
        """
        Create a popup
        
        Args:
            x, y: Position (centered if x/y are screen center)
            width, height: Size of popup
            title: Title text
            message: Message text
            font_manager: FontManager instance
            button_text: Text for OK button
            callback: Function to call when OK is clicked
            add_gold_callback: Optional callback to add gold (for insufficient funds)
            pokedollar_icon: Optional icon for add gold button
        """
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.title = title
        self.message = message
        self.font_manager = font_manager
        self.button_text = button_text
        self.callback = callback
        self.add_gold_callback = add_gold_callback
        self.pokedollar_icon = pokedollar_icon
        
        # Colors
        self.bg_color = (40, 40, 50)
        self.title_bg_color = (60, 60, 70)
        self.border_color = (200, 200, 200)
        self.text_color = (255, 255, 255)
        
        # Create buttons
        from ui.button import Button
        button_width = 220  # Increased from 120 to 220 (100px bigger)
        button_height = 40
        button_y = self.rect.bottom - button_height - 20
        
        if add_gold_callback:
            # Two buttons: Add Gold and OK
            self.add_gold_button = Button(
                self.rect.centerx - button_width - 10,
                button_y,
                button_width,
                button_height,
                "",  # Empty text, we'll render currency on top
                font_manager,
                font_size=18,
                use_title_font=True,
                bg_color=(0, 150, 0),
                hover_color=(0, 200, 0),
                callback=self._add_gold_and_close
            )
            
            self.ok_button = Button(
                self.rect.centerx + 10,
                button_y,
                button_width,
                button_height,
                button_text,
                font_manager,
                font_size=20,
                use_title_font=True,
                callback=self._on_ok_clicked
            )
        else:
            # Single OK button
            self.add_gold_button = None
            button_x = self.rect.centerx - button_width // 2
            self.ok_button = Button(
                button_x, button_y,
                button_width, button_height,
                button_text,
                font_manager,
                font_size=20,
                use_title_font=True,
                callback=self._on_ok_clicked
            )
        
        self.is_visible = True
    
    def _add_gold_and_close(self):
        """Add gold and close popup"""
        if self.add_gold_callback:
            self.add_gold_callback()
        self._on_ok_clicked()
    
    def _on_ok_clicked(self):
        """Handle OK button click"""
        self.is_visible = False
        if self.callback:
            self.callback()
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle events
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled
        """
        if not self.is_visible:
            return False
        
        # Pass to buttons
        if self.ok_button.handle_event(event):
            return True
        if self.add_gold_button and self.add_gold_button.handle_event(event):
            return True
        
        # ESC or Enter to close
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self._on_ok_clicked()
                return True
        
        # Block all events when popup is visible
        return True
    
    def update(self):
        """Update popup"""
        if self.is_visible:
            self.ok_button.update()
            if self.add_gold_button:
                self.add_gold_button.update()
    
    def render(self, surface: pygame.Surface):
        """
        Render the popup
        
        Args:
            surface: Surface to draw on
        """
        if not self.is_visible:
            return
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # 70% opacity black
        surface.blit(overlay, (0, 0))
        
        # Draw popup background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 3)
        
        # Draw title bar
        title_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 50)
        pygame.draw.rect(surface, self.title_bg_color, title_rect)
        pygame.draw.line(surface, self.border_color, 
                        (title_rect.left, title_rect.bottom), 
                        (title_rect.right, title_rect.bottom), 2)
        
        # Draw title
        if self.font_manager:
            title_surface = self.font_manager.render_text(
                self.title, 24, self.text_color, is_title=True
            )
            title_text_rect = title_surface.get_rect(center=title_rect.center)
            surface.blit(title_surface, title_text_rect)
        
        # Draw message (word wrap)
        if self.font_manager:
            message_y = self.rect.y + 70
            message_x = self.rect.x + 20
            max_width = self.rect.width - 40
            
            # Simple word wrap
            words = self.message.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                text_width, _ = self.font_manager.get_text_size(test_line, 18)
                
                if text_width <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Render lines
            for i, line in enumerate(lines):
                line_surface = self.font_manager.render_text(line, 18, self.text_color)
                surface.blit(line_surface, (message_x, message_y + i * 25))
        
        # Draw buttons
        if self.add_gold_button:
            self.add_gold_button.render(surface)
            
            # Draw currency on add gold button
            if self.pokedollar_icon and self.font_manager:
                button_center_x = self.add_gold_button.rect.centerx
                button_center_y = self.add_gold_button.rect.centery
                
                CurrencyDisplay.render_centered(
                    surface,
                    button_center_x,
                    button_center_y,
                    20000,
                    self.pokedollar_icon,
                    self.font_manager,
                    font_size=18,
                    color=(255, 255, 255),
                    icon_size=18
                )
        
        self.ok_button.render(surface)
    
    def show(self):
        """Show the popup"""
        self.is_visible = True
    
    def hide(self):
        """Hide the popup"""
        self.is_visible = False
    
    def is_showing(self) -> bool:
        """Check if popup is visible"""
        return self.is_visible

