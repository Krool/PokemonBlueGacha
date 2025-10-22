"""
Loading screen state - loads all game assets
"""
import pygame
import math
from .base_state import GameState
from config import (COLOR_WHITE, COLOR_BLACK, LOGO_PATH, GACHA_RED_PATH, 
                    GACHA_BLUE_PATH, GACHA_YELLOW_PATH, GACHA_ITEM_PATH, POKEDOLLAR_ICON_PATH, RAYS_PATH, SOUNDS_PATH, LOADING_TIME)


class LoadingState(GameState):
    """Loading screen - displays logo and progress bar while loading assets"""
    
    def enter(self, **kwargs):
        """Initialize loading state"""
        self.progress = 0.0
        self.loading_complete = False
        self.load_stage = 0
        self.load_stages = [
            "Loading UI images...",
            "Loading Pokémon sprites...",
            "Loading audio...",
            "Complete!"
        ]
        self.current_stage_text = self.load_stages[0]
        self.showing_complete = False
        
        # Async loading state
        self.pokemon_index = 0
        self.types_loaded = False
        self.ui_loaded = False
        self.audio_loaded = False
        
        # Try to load logo for display
        try:
            self.logo = self.resource_manager.load_image(LOGO_PATH)
            # Scale logo to reasonable size
            logo_width = min(400, self.logo.get_width())
            logo_height = int(self.logo.get_height() * (logo_width / self.logo.get_width()))
            self.logo = pygame.transform.scale(self.logo, (logo_width, logo_height))
        except:
            self.logo = None
        
        print("Entered LoadingState")
    
    def exit(self):
        """Clean up loading state"""
        print("Exited LoadingState")
    
    def handle_events(self, events):
        """Handle events during loading"""
        for event in events:
            # Enable audio on any user interaction (for web browser autoplay policy)
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                # Don't auto-start music if muted
                allow_music = not self.game_data.music_muted
                self.audio_manager.enable_audio_after_interaction(allow_music_start=allow_music)
                
                # If loading is complete, transition to game on click/keypress
                if self.loading_complete and self.showing_complete:
                    self.state_manager.change_state('inventory')
    
    def update(self, dt):
        """Update loading progress - loads assets gradually over multiple frames"""
        if self.loading_complete:
            # Wait for user interaction - no auto-transition
            # This ensures audio works properly on web
            return
        
        # Stage 0: Load UI images
        if self.load_stage == 0:
            self.current_stage_text = self.load_stages[0]
            if not self.ui_loaded:
                self.resource_manager.load_ui_images(
                    LOGO_PATH, GACHA_RED_PATH, GACHA_BLUE_PATH, GACHA_YELLOW_PATH, 
                    GACHA_ITEM_PATH, POKEDOLLAR_ICON_PATH, RAYS_PATH
                )
                self.ui_loaded = True
                self.progress = 0.1
            else:
                self.load_stage = 1
        
        # Stage 1: Load Pokemon sprites (gradually)
        elif self.load_stage == 1:
            self.current_stage_text = self.load_stages[1]
            
            # Load Pokemon sprites in batches for smoother progress
            pokemon_list = self.resource_manager.pokemon_list
            batch_size = 5  # Load 5 Pokemon per frame
            
            if self.pokemon_index < len(pokemon_list):
                end_index = min(self.pokemon_index + batch_size, len(pokemon_list))
                for i in range(self.pokemon_index, end_index):
                    self.resource_manager.load_image(pokemon_list[i].image_path)
                self.pokemon_index = end_index
                
                # Update progress (UI=10%, Pokemon=70%, Audio=20%)
                pokemon_progress = (self.pokemon_index / len(pokemon_list)) * 0.7
                self.progress = 0.1 + pokemon_progress
            else:
                # Pokemon loading complete, move to types
                if not self.types_loaded:
                    for type_name, poke_type in self.resource_manager.types_dict.items():
                        self.resource_manager.load_image(poke_type.image_path)
                    self.types_loaded = True
                    self.progress = 0.8
                else:
                    self.load_stage = 2
        
        # Stage 2: Load audio
        elif self.load_stage == 2:
            self.current_stage_text = self.load_stages[2]
            if not self.audio_loaded:
                self.audio_manager.load_game_sounds(SOUNDS_PATH)
                self.audio_manager.load_background_music_tracks(SOUNDS_PATH)
                self.audio_manager.play_random_background_music()
                self.audio_loaded = True
                self.progress = 0.95
            else:
                self.load_stage = 3
        
        # Stage 3: Complete
        elif self.load_stage == 3:
            self.current_stage_text = self.load_stages[3]
            self.progress = 1.0
            self.loading_complete = True
            self.showing_complete = True
    
    def render(self):
        """Render loading screen"""
        self.screen.fill(COLOR_BLACK)
        
        # Display logo as full-screen background if available
        if self.logo:
            # Scale logo to cover the entire screen
            logo_scaled = pygame.transform.scale(self.logo, (self.screen.get_width(), self.screen.get_height()))
            self.screen.blit(logo_scaled, (0, 0))
            
            # Add a semi-transparent dark overlay for better text readability
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Darker overlay for better contrast
            self.screen.blit(overlay, (0, 0))
        
        # Center Y position for loading elements
        center_y = self.screen.get_height() // 2
        
        # Stage text (smaller and above progress bar)
        font_stage = pygame.font.Font(None, 28)
        stage_text = font_stage.render(self.current_stage_text, True, (200, 200, 200))
        stage_rect = stage_text.get_rect(center=(self.screen.get_width() // 2, center_y - 60))
        self.screen.blit(stage_text, stage_rect)
        
        # Draw progress bar
        bar_width = min(600, self.screen.get_width() - 100)
        bar_height = 40
        bar_x = (self.screen.get_width() - bar_width) // 2
        bar_y = center_y - 20
        
        # Background (dark gray)
        pygame.draw.rect(self.screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        
        # Progress fill with gradient effect
        progress_width = int(bar_width * self.progress)
        if progress_width > 0:
            # Main progress bar (blue-ish white)
            pygame.draw.rect(self.screen, (100, 149, 237), (bar_x, bar_y, progress_width, bar_height), border_radius=5)
            # Lighter inner highlight
            if progress_width > 4:
                pygame.draw.rect(self.screen, (150, 180, 255), (bar_x, bar_y, progress_width, bar_height // 3), border_radius=5)
        
        # Border (white)
        pygame.draw.rect(self.screen, COLOR_WHITE, (bar_x, bar_y, bar_width, bar_height), 3, border_radius=5)
        
        # Percentage text (inside or next to bar)
        font_percent = pygame.font.Font(None, 36)
        percent_text = font_percent.render(f"{int(self.progress * 100)}%", True, COLOR_WHITE)
        percent_rect = percent_text.get_rect(center=(self.screen.get_width() // 2, bar_y + bar_height + 35))
        self.screen.blit(percent_text, percent_rect)
        
        # Instruction text if complete
        if self.loading_complete:
            font_instruction = pygame.font.Font(None, 40)
            instruction = font_instruction.render("Click or press any key to start", True, (100, 255, 100))
            instruction_rect = instruction.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 100))
            
            # Add a subtle pulsing effect
            pulse = abs(math.sin(pygame.time.get_ticks() / 500.0))
            instruction.set_alpha(int(155 + pulse * 100))
            
            self.screen.blit(instruction, instruction_rect)

