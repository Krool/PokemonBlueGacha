"""
Currency display component - renders amount with Pokédollar icon
"""
import pygame


class CurrencyDisplay:
    """Helper for displaying currency with icon"""
    
    @staticmethod
    def render(surface: pygame.Surface, x: int, y: int, amount: int, 
               icon: pygame.Surface, font_manager, font_size: int = 24,
               color: tuple = (255, 255, 255), icon_size: int = 24,
               spacing: int = 5, align: str = "left") -> pygame.Rect:
        """
        Render currency amount with Pokédollar icon
        
        Args:
            surface: Surface to draw on
            x, y: Position (depends on align)
            amount: Currency amount to display
            icon: Pokédollar icon image
            font_manager: FontManager instance
            font_size: Font size for text
            color: Text color
            icon_size: Size to scale icon to
            spacing: Space between icon and text
            align: "left" or "right" alignment
            
        Returns:
            Rect of the rendered currency display
        """
        # Scale icon
        scaled_icon = pygame.transform.scale(icon, (icon_size, icon_size))
        
        # Render amount text
        amount_text = f"{amount:,}"  # Format with commas
        text_surface = font_manager.render_text(amount_text, font_size, color)
        
        # Calculate total width
        total_width = scaled_icon.get_width() + spacing + text_surface.get_width()
        
        # Adjust position based on alignment
        if align == "right":
            draw_x = x - total_width
        else:
            draw_x = x
        
        # Draw icon
        icon_y = y - (scaled_icon.get_height() // 2) + (font_size // 2)
        surface.blit(scaled_icon, (draw_x, icon_y))
        
        # Draw text
        text_x = draw_x + scaled_icon.get_width() + spacing
        text_y = y - (text_surface.get_height() // 2) + (font_size // 2)
        surface.blit(text_surface, (text_x, text_y))
        
        # Return bounding rect
        return pygame.Rect(draw_x, min(icon_y, text_y), 
                          total_width, max(scaled_icon.get_height(), text_surface.get_height()))
    
    @staticmethod
    def render_centered(surface: pygame.Surface, center_x: int, y: int, amount: int,
                       icon: pygame.Surface, font_manager, font_size: int = 24,
                       color: tuple = (255, 255, 255), icon_size: int = 24,
                       spacing: int = 5) -> pygame.Rect:
        """
        Render currency centered at a point
        
        Args:
            surface: Surface to draw on
            center_x: X coordinate of center
            y: Y coordinate
            amount: Currency amount
            icon: Pokédollar icon
            font_manager: FontManager instance
            font_size: Font size
            color: Text color
            icon_size: Icon size
            spacing: Space between icon and text
            
        Returns:
            Rect of the rendered currency display
        """
        # Scale icon
        scaled_icon = pygame.transform.scale(icon, (icon_size, icon_size))
        
        # Render text
        amount_text = f"{amount:,}"
        text_surface = font_manager.render_text(amount_text, font_size, color)
        
        # Calculate total width
        total_width = scaled_icon.get_width() + spacing + text_surface.get_width()
        
        # Calculate starting X to center
        draw_x = center_x - (total_width // 2)
        
        # Draw icon
        icon_y = y - (scaled_icon.get_height() // 2) + (font_size // 2)
        surface.blit(scaled_icon, (draw_x, icon_y))
        
        # Draw text
        text_x = draw_x + scaled_icon.get_width() + spacing
        text_y = y - (text_surface.get_height() // 2) + (font_size // 2)
        surface.blit(text_surface, (text_x, text_y))
        
        # Return bounding rect
        return pygame.Rect(draw_x, min(icon_y, text_y),
                          total_width, max(scaled_icon.get_height(), text_surface.get_height()))

