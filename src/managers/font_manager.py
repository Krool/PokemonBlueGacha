"""
Font management for consistent text rendering
"""
import pygame
import os


class FontManager:
    """Manages font loading and rendering"""
    
    def __init__(self, title_font_path: str, body_font_path: str):
        """
        Initialize font manager
        
        Args:
            title_font_path: Path to the title font file
            body_font_path: Path to the body text font file
        """
        self.title_font_path = title_font_path
        self.body_font_path = body_font_path
        self.title_fonts = {}  # Cache for title font sizes
        self.body_fonts = {}   # Cache for body font sizes
        
        # Check if custom fonts exist
        if not os.path.exists(title_font_path):
            print(f"Warning: Title font not found at {title_font_path}, using default")
            self.title_font_path = None
        
        if not os.path.exists(body_font_path):
            print(f"Warning: Body font not found at {body_font_path}, using default")
            self.body_font_path = None
    
    def get_font(self, size: int, is_title: bool = False) -> pygame.font.Font:
        """
        Get a font of the specified size (cached)
        
        Args:
            size: Font size in pixels
            is_title: If True, use title font; otherwise use body font
            
        Returns:
            pygame.font.Font object
        """
        font_cache = self.title_fonts if is_title else self.body_fonts
        font_path = self.title_font_path if is_title else self.body_font_path
        
        if size not in font_cache:
            if font_path:
                try:
                    font_cache[size] = pygame.font.Font(font_path, size)
                except Exception as e:
                    print(f"Error loading custom font: {e}, using default")
                    font_cache[size] = pygame.font.Font(None, size)
            else:
                font_cache[size] = pygame.font.Font(None, size)
        
        return font_cache[size]
    
    def get_title_font(self, size: int) -> pygame.font.Font:
        """
        Get title font of specified size
        
        Args:
            size: Font size in pixels
            
        Returns:
            pygame.font.Font object
        """
        return self.get_font(size, is_title=True)
    
    def get_body_font(self, size: int) -> pygame.font.Font:
        """
        Get body font of specified size
        
        Args:
            size: Font size in pixels
            
        Returns:
            pygame.font.Font object
        """
        return self.get_font(size, is_title=False)
    
    def render_text(self, text: str, size: int, color: tuple, 
                    antialias: bool = True, is_title: bool = False) -> pygame.Surface:
        """
        Render text to a surface
        
        Args:
            text: Text to render
            size: Font size
            color: RGB color tuple
            antialias: Whether to use antialiasing
            is_title: If True, use title font; otherwise use body font
            
        Returns:
            Rendered text surface
        """
        font = self.get_font(size, is_title=is_title)
        return font.render(text, antialias, color)
    
    def render_text_centered(self, text: str, size: int, color: tuple,
                            rect: pygame.Rect, antialias: bool = True, is_title: bool = False) -> tuple:
        """
        Render text centered within a rect
        
        Args:
            text: Text to render
            size: Font size
            color: RGB color tuple
            rect: Rectangle to center within
            antialias: Whether to use antialiasing
            is_title: If True, use title font; otherwise use body font
            
        Returns:
            Tuple of (surface, position) where position is top-left for centering
        """
        surface = self.render_text(text, size, color, antialias, is_title=is_title)
        text_rect = surface.get_rect(center=rect.center)
        return surface, text_rect.topleft
    
    def get_text_size(self, text: str, size: int, is_title: bool = False) -> tuple:
        """
        Get the size of rendered text without actually rendering
        
        Args:
            text: Text to measure
            size: Font size
            is_title: If True, use title font; otherwise use body font
            
        Returns:
            Tuple of (width, height)
        """
        font = self.get_font(size, is_title=is_title)
        return font.size(text)

