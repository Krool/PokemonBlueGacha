"""
Scrollable Grid UI Component for Pokemon tiles
"""
import pygame
from typing import List
from ui.pokemon_tile import PokemonTile


class ScrollableGrid:
    """Scrollable grid of Pokemon tiles"""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 tile_width: int, tile_height: int, 
                 columns: int, spacing_x: int, spacing_y: int):
        """
        Create a scrollable grid
        
        Args:
            x, y: Top-left position of grid area
            width, height: Size of visible area
            tile_width, tile_height: Size of each tile
            columns: Number of tiles per row
            spacing_x, spacing_y: Spacing between tiles
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.columns = columns
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y
        
        self.scroll_offset = 0
        self.max_scroll = 0
        
        self.tiles: List[PokemonTile] = []
        self.pokemon_list = []
    
    def set_pokemon_list(self, pokemon_list, resource_manager, font_manager, game_data):
        """
        Set the list of Pokemon to display
        
        Args:
            pokemon_list: List of Pokemon objects
            resource_manager: ResourceManager for images/data
            font_manager: FontManager for text
            game_data: GameData for owned counts
        """
        self.pokemon_list = pokemon_list
        self.tiles = []
        
        # Create tiles for each Pokemon
        for i, pokemon in enumerate(pokemon_list):
            row = i // self.columns
            col = i % self.columns
            
            x = self.rect.x + col * (self.tile_width + self.spacing_x)
            y = self.rect.y + row * (self.tile_height + self.spacing_y)
            
            # Check if owned
            owned_count = game_data.pokemon_owned.get(pokemon.number, 0)
            is_owned = owned_count > 0
            
            tile = PokemonTile(
                x, y, self.tile_width, self.tile_height,
                pokemon,
                resource_manager,
                font_manager,
                show_new_badge=False,
                show_count=is_owned,
                count=owned_count
            )
            
            # Add grayed_out attribute for unowned Pokemon
            tile.grayed_out = not is_owned
            
            self.tiles.append(tile)
        
        # Calculate max scroll
        total_rows = (len(pokemon_list) + self.columns - 1) // self.columns
        total_height = total_rows * (self.tile_height + self.spacing_y)
        self.max_scroll = max(0, total_height - self.rect.height)
    
    def handle_event(self, event: pygame.event.Event):
        """
        Handle scroll events
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.MOUSEWHEEL:
            # Check if mouse is over grid area
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                # Scroll (negative y means scroll up, positive means scroll down)
                self.scroll_offset -= event.y * 30  # 30 pixels per scroll
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
    
    def get_clicked_pokemon(self, mouse_pos):
        """
        Get the Pokemon that was clicked at the given mouse position
        
        Args:
            mouse_pos: Mouse position (x, y)
            
        Returns:
            Pokemon object if clicked, None otherwise
        """
        # Check if click is within grid area
        if not self.rect.collidepoint(mouse_pos):
            return None
            
        # Check each tile
        for i, tile in enumerate(self.tiles):
            # Calculate adjusted position based on scroll
            adjusted_y = tile.rect.y - self.scroll_offset
            
            # Create a temporary rect at the adjusted position
            adjusted_rect = pygame.Rect(tile.rect.x, adjusted_y, tile.rect.width, tile.rect.height)
            
            # Check if mouse is over this tile and tile is visible
            if adjusted_rect.collidepoint(mouse_pos):
                if adjusted_y + tile.rect.height >= self.rect.y and adjusted_y <= self.rect.bottom:
                    return tile.pokemon
        
        return None
    
    def update(self, dt):
        """Update grid (currently unused)"""
        pass
    
    def render(self, surface: pygame.Surface):
        """
        Render the visible tiles
        
        Args:
            surface: Surface to draw on
        """
        # Create a clipping rect for the grid area
        clip_rect = surface.get_clip()
        surface.set_clip(self.rect)
        
        # Render tiles with scroll offset
        for tile in self.tiles:
            # Calculate adjusted position based on scroll
            adjusted_y = tile.rect.y - self.scroll_offset
            
            # Only render if visible in the grid area
            if adjusted_y + tile.rect.height >= self.rect.y and adjusted_y <= self.rect.bottom:
                # Temporarily adjust tile position
                original_y = tile.rect.y
                tile.rect.y = adjusted_y
                
                # Render tile (handle grayed_out if attribute exists)
                if hasattr(tile, 'grayed_out') and tile.grayed_out:
                    self._render_grayed_tile(surface, tile)
                else:
                    tile.render(surface)
                
                # Restore original position
                tile.rect.y = original_y
        
        # Restore original clip rect
        surface.set_clip(clip_rect)
        
        # Draw border around grid area (optional)
        # pygame.draw.rect(surface, (100, 100, 100), self.rect, 2)
    
    def _render_grayed_tile(self, surface: pygame.Surface, tile: PokemonTile):
        """
        Render a grayed-out tile for unowned Pokemon
        
        Args:
            surface: Surface to draw on
            tile: PokemonTile to render
        """
        # Create a temporary surface for the tile
        temp_surface = pygame.Surface((tile.rect.width, tile.rect.height), pygame.SRCALPHA)
        
        # Render tile normally to temp surface
        temp_surface.fill((0, 0, 0, 0))  # Clear with transparency
        
        # Draw background
        bg_color = (30, 30, 40)
        pygame.draw.rect(temp_surface, bg_color, pygame.Rect(0, 0, tile.rect.width, tile.rect.height))
        
        # Draw dashed border (unowned)
        border_color = (100, 100, 100)
        rect = pygame.Rect(0, 0, tile.rect.width, tile.rect.height)
        
        # Top and bottom
        for x in range(0, tile.rect.width, 10):
            pygame.draw.line(temp_surface, border_color, (x, 0), (min(x + 5, tile.rect.width), 0), 2)
            pygame.draw.line(temp_surface, border_color, (x, tile.rect.height - 1), (min(x + 5, tile.rect.width), tile.rect.height - 1), 2)
        
        # Left and right
        for y in range(0, tile.rect.height, 10):
            pygame.draw.line(temp_surface, border_color, (0, y), (0, min(y + 5, tile.rect.height)), 2)
            pygame.draw.line(temp_surface, border_color, (tile.rect.width - 1, y), (tile.rect.width - 1, min(y + 5, tile.rect.height)), 2)
        
        # Draw Pokemon image (grayed)
        image = tile.resource_manager.images.get(tile.pokemon.image_path)
        if image:
            img_size = min(tile.rect.width - 20, tile.rect.height - 60)
            scaled_image = pygame.transform.scale(image, (img_size, img_size))
            
            # Make it gray
            gray_image = scaled_image.copy()
            gray_image.set_alpha(80)  # 30% opacity
            
            img_x = (tile.rect.width - img_size) // 2
            img_y = 10
            temp_surface.blit(gray_image, (img_x, img_y))
        
        # Draw "???" instead of name
        name_y = tile.rect.height - 45
        if tile.font_manager:
            name_surface = tile.font_manager.render_text("???", 12, (120, 120, 120))
            name_rect = name_surface.get_rect(center=(tile.rect.width // 2, name_y))
            temp_surface.blit(name_surface, name_rect)
        
        # Draw Pokédex number
        number_y = tile.rect.height - 25
        if tile.font_manager:
            number_text = f"#{tile.pokemon.number}"
            number_surface = tile.font_manager.render_text(number_text, 12, (100, 100, 100))
            number_rect = number_surface.get_rect(center=(tile.rect.width // 2, number_y))
            temp_surface.blit(number_surface, number_rect)
        
        # Blit temp surface to main surface
        surface.blit(temp_surface, tile.rect.topleft)
    
    def get_scroll_percentage(self) -> float:
        """Get current scroll position as percentage (0.0 to 1.0)"""
        if self.max_scroll == 0:
            return 0.0
        return self.scroll_offset / self.max_scroll

