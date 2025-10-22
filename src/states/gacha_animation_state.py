"""
Gacha Animation State - Shows exciting reveal animation
"""
import pygame
import math
import random
from states.base_state import GameState
from config import COLOR_WHITE, COLOR_BLACK, SCREEN_WIDTH, SCREEN_HEIGHT

class GachaAnimationState(GameState):
    """State for animating the gacha pull result"""
    
    def __init__(self, state_manager, game_data, resource_manager, audio_manager, font_manager=None, gacha_system=None):
        super().__init__(state_manager, game_data, resource_manager, audio_manager, font_manager, gacha_system)
        self.results = []  # List of Pokemon/Item objects
        self.is_ten_pull = False
        self.is_items_gacha = False
        self.current_index = 0  # Which result we're showing (for 10-pull)
        self.animation_time = 0.0
        self.duration = 0.0  # Set based on rarity
        self.rarity_obj = None
        self.sound_played = False
        self.owned_before = 0  # Count of owned Pokemon before this pull
        
    def enter(self, results=None, is_ten_pull=False, machine=None, owned_before=0, is_items_gacha=False):
        """
        Enter the animation state
        
        Args:
            results: List of Pokemon/Item objects from gacha roll
            is_ten_pull: Whether this was a 10-pull (show all at once) or single pull
            machine: Which gacha machine was used (Red, Blue, Yellow, Items)
            owned_before: Count of owned Pokemon before this pull (0 for items)
            is_items_gacha: Whether this is an items gacha
        """
        print("Entered GachaAnimationState")
        
        # Enable audio immediately on entry (user just clicked to pull)
        # Don't auto-start music if muted
        allow_music = not self.game_data.music_muted
        self.audio_manager.enable_audio_after_interaction(allow_music_start=allow_music)
        
        if results is None:
            results = []
        
        self.results = results
        self.is_ten_pull = is_ten_pull
        self.is_items_gacha = is_items_gacha
        self.machine = machine if machine else "Red"
        self.current_index = 0
        self.animation_time = 0.0
        self.sound_played = False
        self.owned_before = owned_before
        
        if not is_ten_pull and len(results) > 0:
            # Single pull - animate the first (only) result
            result = results[0]
            self.rarity_obj = self.resource_manager.rarities_dict.get(result.rarity)
            self.duration = self._get_animation_duration(result.rarity)
            self._play_rarity_sound(result.rarity)
            self.sound_played = True
        elif is_ten_pull and len(results) > 0:
            # 10-pull - find highest rarity for sound/duration
            highest_rarity = self._get_highest_rarity(results)
            self.rarity_obj = self.resource_manager.rarities_dict.get(highest_rarity)
            self.duration = self._get_animation_duration(highest_rarity)
            self._play_rarity_sound(highest_rarity)
            self.sound_played = True
        else:
            # Fallback
            self.duration = 1.0
    
    def exit(self):
        """Clean up when leaving state"""
        print("Exited GachaAnimationState")
    
    def _get_animation_duration(self, rarity: str) -> float:
        """Get animation duration based on rarity (in seconds)"""
        durations = {
            "Common": 0.8,
            "Uncommon": 1.0,
            "Rare": 1.3,
            "Epic": 1.6,
            "Legendary": 2.0
        }
        return durations.get(rarity, 1.0)
    
    def _get_highest_rarity(self, results) -> str:
        """Get the highest rarity from a list of Pokemon"""
        rarity_order = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
        highest = "Common"
        highest_index = 0
        
        for pokemon in results:
            if pokemon.rarity in rarity_order:
                index = rarity_order.index(pokemon.rarity)
                if index > highest_index:
                    highest_index = index
                    highest = pokemon.rarity
        
        return highest
    
    def _play_rarity_sound(self, rarity: str):
        """Play sound effect based on rarity"""
        if rarity == "Legendary":
            self.audio_manager.play_sound("legendary")
            # Also play chaching sound for extra excitement on legendary pulls
            self.audio_manager.play_sound("chaching")
        else:
            # Randomly pick roll1, roll2, or roll3
            roll_sfx = random.choice(["roll1", "roll2", "roll3"])
            self.audio_manager.play_sound(roll_sfx)
    
    def handle_events(self, events):
        """Handle input events"""
        # Enable audio on any user interaction (for web browser autoplay policy)
        for event in events:
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                # Don't auto-start music if muted
                allow_music = not self.game_data.music_muted
                self.audio_manager.enable_audio_after_interaction(allow_music_start=allow_music)
                break
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Skip animation
                    self._finish_animation()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Click to skip
                self._finish_animation()
    
    def _finish_animation(self):
        """Finish animation and transition to outcome"""
        self.state_manager.change_state('gacha_outcome', 
                                        results=self.results, 
                                        is_ten_pull=self.is_ten_pull,
                                        machine=self.machine,
                                        is_items_gacha=self.is_items_gacha,
                                        owned_before=self.owned_before)
    
    def update(self, dt):
        """Update animation"""
        self.animation_time += dt
        
        # Check if animation is complete
        if self.animation_time >= self.duration:
            self._finish_animation()
    
    def render(self):
        """Render the animation"""
        self.screen.fill(COLOR_BLACK)
        
        if not self.results:
            return
        
        # Get progress (0.0 to 1.0)
        progress = min(self.animation_time / self.duration, 1.0) if self.duration > 0 else 1.0
        
        if self.is_ten_pull:
            self._render_ten_pull_animation(self.screen, progress)
        else:
            self._render_single_pull_animation(self.screen, progress)
        
        # Draw skip hint
        skip_text = "Click or press SPACE to skip"
        if self.font_manager:
            text_surface = self.font_manager.render_text(skip_text, 18, COLOR_WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            self.screen.blit(text_surface, text_rect)
    
    def _render_single_pull_animation(self, screen, progress):
        """Render animation for a single pull"""
        if len(self.results) == 0:
            return
        
        result = self.results[0]  # Can be Pokemon or Item
        rarity_color = self.rarity_obj.get_color_rgb() if self.rarity_obj else (255, 255, 255)
        
        # Render rays background effect
        if hasattr(self.resource_manager, 'rays') and self.resource_manager.rays:
            self._render_rays_effect(screen, result.rarity, rarity_color, progress)
        
        # Get image (Pokemon sprite or item icon)
        if self.is_items_gacha:
            image = self.resource_manager.get_item_icon(result.number)
        else:
            image = self.resource_manager.images.get(result.image_path)
        
        if not image:
            return
        
        # Scale image
        base_size = 200
        image = pygame.transform.scale(image, (base_size, base_size))
        
        # Apply effects based on progress and rarity
        image = self._apply_animation_effects(image, result.rarity, progress)
        
        # Position in center
        x = SCREEN_WIDTH // 2 - image.get_width() // 2
        y = SCREEN_HEIGHT // 2 - image.get_height() // 2
        
        screen.blit(image, (x, y))
        
        # Draw rarity text (fades in)
        if progress > 0.5 and self.rarity_obj:
            alpha = int(min((progress - 0.5) * 2, 1.0) * 255)
            
            if self.font_manager:
                rarity_text = result.rarity.upper()
                text_surface = self.font_manager.render_text(rarity_text, 36, rarity_color, is_title=True)
                text_surface.set_alpha(alpha)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
                screen.blit(text_surface, text_rect)
    
    def _render_ten_pull_animation(self, screen, progress):
        """Render animation for a 10-pull (all at once)"""
        # Show all 10 Pokemon/Items appearing with a wave effect
        for i, result in enumerate(self.results):
            # Stagger appearance
            item_progress = max(0, min((progress * 1.5 - i * 0.05), 1.0))
            
            if item_progress <= 0:
                continue
            
            # Position in grid (2 rows of 5)
            col = i % 5
            row = i // 5
            spacing_x = 100
            spacing_y = 120
            start_x = SCREEN_WIDTH // 2 - (spacing_x * 5) // 2 + spacing_x // 2
            start_y = SCREEN_HEIGHT // 2 - spacing_y
            
            center_x = start_x + col * spacing_x
            center_y = start_y + row * spacing_y
            
            # Render individual rays behind this result
            if hasattr(self.resource_manager, 'rays') and self.resource_manager.rays:
                rarity_obj = self.resource_manager.rarities_dict.get(result.rarity)
                if rarity_obj:
                    rarity_color = rarity_obj.get_color_rgb()
                    self._render_rays_effect_at_position(screen, result.rarity, rarity_color, item_progress, center_x, center_y, scale_multiplier=0.4)
            
            # Get image (Pokemon sprite or item icon)
            if self.is_items_gacha:
                image = self.resource_manager.get_item_icon(result.number)
            else:
                image = self.resource_manager.images.get(result.image_path)
            
            if not image:
                continue
            
            # Scale smaller for 10-pull
            size = 80
            image = pygame.transform.scale(image, (size, size))
            
            # Apply scale-up effect during appearance
            if item_progress < 1.0:
                scale_factor = 0.5 + item_progress * 0.5
                new_size = int(size * scale_factor)
                image = pygame.transform.scale(image, (new_size, new_size))
            
            # Apply the same animation effects as single pull (rotation, shake, tint)
            # Use item_progress so each result animates independently
            image = self._apply_animation_effects(image, result.rarity, item_progress)
            
            x = center_x - image.get_width() // 2
            y = center_y - image.get_height() // 2
            
            screen.blit(image, (x, y))
        
        # Draw "10-PULL!" text
        if progress > 0.3 and self.font_manager:
            alpha = int(min((progress - 0.3) / 0.7, 1.0) * 255)
            rarity_color = self.rarity_obj.get_color_rgb() if self.rarity_obj else COLOR_WHITE
            
            text_surface = self.font_manager.render_text("10-PULL!", 48, rarity_color, is_title=True)
            text_surface.set_alpha(alpha)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
            screen.blit(text_surface, text_rect)
    
    def _render_rays_effect(self, screen, rarity: str, rarity_color: tuple, progress: float):
        """
        Render rays background effect with rarity-based scaling and colorization
        
        Args:
            screen: Surface to render on
            rarity: Pokemon rarity ("Common", "Uncommon", "Rare", "Epic", "Legendary")
            rarity_color: RGB color tuple for the rarity
            progress: Animation progress (0.0 to 1.0)
        """
        # Scale based on rarity (50% smaller than original for better visibility balance)
        # Pokemon sprite is 200px
        scale_by_rarity = {
            "Common": 1.25,     # 250px (25% bigger than Pokemon)
            "Uncommon": 1.5,    # 300px (50% bigger)
            "Rare": 1.75,       # 350px (75% bigger)
            "Epic": 2.0,        # 400px (100% bigger)
            "Legendary": 2.5    # 500px (150% bigger)
        }
        scale = scale_by_rarity.get(rarity, 1.25)
        
        # Get rays image
        rays = self.resource_manager.rays
        if not rays:
            return
        
        # Calculate size - base size is now 200px (matching Pokemon sprite size)
        base_size = 200  # Base size matches Pokemon sprite
        scaled_size = int(base_size * scale)
        
        # Scale rays
        scaled_rays = pygame.transform.scale(rays, (scaled_size, scaled_size))
        
        # Create a copy for colorization
        colorized_rays = scaled_rays.copy()
        
        # Apply rarity color tint using additive blending for brightness
        color_overlay = pygame.Surface(colorized_rays.get_size(), pygame.SRCALPHA)
        # Much stronger tint for visibility
        tint_strength = {
            "Common": 100,      # Increased from 30
            "Uncommon": 130,    # Increased from 50
            "Rare": 160,        # Increased from 80
            "Epic": 200,        # Increased from 120
            "Legendary": 255    # Increased from 180
        }
        alpha = tint_strength.get(rarity, 100)
        color_overlay.fill((*rarity_color, alpha))
        # Use ADD blend mode for brighter, more visible rays
        colorized_rays.blit(color_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        # Rotate rays based on animation progress (creates spinning effect)
        rotation_speed = 360 / self.duration  # One full rotation per animation
        angle = (self.animation_time * rotation_speed) % 360
        rotated_rays = pygame.transform.rotate(colorized_rays, angle)
        
        # Set opacity (make it more visible - don't fade in, just make it slightly transparent)
        rotated_rays.set_alpha(200)  # 200/255 = ~78% opacity, always visible
        
        # Center the rays
        rays_rect = rotated_rays.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(rotated_rays, rays_rect)
    
    def _render_rays_effect_at_position(self, screen, rarity: str, rarity_color: tuple, progress: float, center_x: int, center_y: int, scale_multiplier: float = 1.0):
        """
        Render rays background effect at a specific position (for 10-pull grid)
        
        Args:
            screen: Surface to render on
            rarity: Pokemon rarity
            rarity_color: RGB color tuple for the rarity
            progress: Animation progress (0.0 to 1.0)
            center_x: X position for center of rays
            center_y: Y position for center of rays
            scale_multiplier: Additional scaling factor (0.4 for 10-pull)
        """
        # Scale based on rarity (adjusted for 10-pull grid)
        scale_by_rarity = {
            "Common": 1.25,
            "Uncommon": 1.5,
            "Rare": 1.75,
            "Epic": 2.0,
            "Legendary": 2.5
        }
        scale = scale_by_rarity.get(rarity, 1.25) * scale_multiplier
        
        # Get rays image
        rays = self.resource_manager.rays
        if not rays:
            return
        
        # Calculate size (base 80px for 10-pull Pokemon)
        base_size = 80
        scaled_size = int(base_size * scale)
        
        # Scale and colorize rays
        scaled_rays = pygame.transform.scale(rays, (scaled_size, scaled_size))
        colorized_rays = scaled_rays.copy()
        
        # Apply rarity color tint
        color_overlay = pygame.Surface(colorized_rays.get_size(), pygame.SRCALPHA)
        tint_strength = {
            "Common": 100,
            "Uncommon": 130,
            "Rare": 160,
            "Epic": 200,
            "Legendary": 255
        }
        alpha = tint_strength.get(rarity, 100)
        color_overlay.fill((*rarity_color, alpha))
        colorized_rays.blit(color_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        # Rotate rays (faster rotation for grid items)
        rotation_speed = 720 / self.duration  # Two full rotations per animation
        angle = (self.animation_time * rotation_speed) % 360
        rotated_rays = pygame.transform.rotate(colorized_rays, angle)
        
        # Set opacity
        rotated_rays.set_alpha(200)
        
        # Position at specific location
        rays_rect = rotated_rays.get_rect(center=(center_x, center_y))
        screen.blit(rotated_rays, rays_rect)
    
    def _apply_animation_effects(self, image, rarity, progress):
        """Apply visual effects to image based on rarity and progress"""
        # Shake intensity based on rarity
        shake_amounts = {
            "Common": 3,
            "Uncommon": 5,
            "Rare": 8,
            "Epic": 12,
            "Legendary": 15
        }
        shake = shake_amounts.get(rarity, 5)
        
        # Rotation for higher rarities
        rotate_rarities = ["Epic", "Legendary"]
        if rarity in rotate_rarities and progress < 0.8:
            # Oscillating rotation
            angle = math.sin(progress * math.pi * 4) * 15 * (1 - progress)
            image = pygame.transform.rotate(image, angle)
        
        # Color tinting based on rarity
        if progress < 0.6:
            rarity_obj = self.resource_manager.rarities_dict.get(rarity)
            if rarity_obj:
                color = rarity_obj.get_color_rgb()
                # Create a colored overlay
                tint_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
                tint_alpha = int((1 - progress / 0.6) * 100)  # Fade out tint
                tint_surface.fill((*color, tint_alpha))
                image = image.copy()
                image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        return image

