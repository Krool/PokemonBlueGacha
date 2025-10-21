"""
Loading screen state - loads all game assets
"""
import pygame
from .base_state import GameState
from config import (COLOR_WHITE, COLOR_BLACK, LOGO_PATH, GACHA_RED_PATH, 
                    GACHA_BLUE_PATH, GACHA_YELLOW_PATH, POKEDOLLAR_ICON_PATH, RAYS_PATH, SOUNDS_PATH, LOADING_TIME)


class LoadingState(GameState):
    """Loading screen - displays logo and progress bar while loading assets"""
    
    def enter(self, **kwargs):
        """Initialize loading state"""
        self.progress = 0.0
        self.loading_complete = False
        self.loading_started = False
        self.load_stage = 0
        self.load_stages = [
            "Loading UI images...",
            "Loading Pokémon sprites...",
            "Loading audio...",
            "Complete!"
        ]
        self.current_stage_text = self.load_stages[0]
        
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
            if event.type == pygame.KEYDOWN and self.loading_complete:
                # Skip to inventory if loading is done
                self.state_manager.change_state('inventory')
    
    def update(self, dt):
        """Update loading progress"""
        if self.loading_complete:
            return
        
        if not self.loading_started:
            # Start loading assets
            self.loading_started = True
            self.load_assets()
        
        # Auto-transition after brief delay to show 100%
        if self.progress >= 1.0:
            self.progress = 1.0
            self.loading_complete = True
            # Brief pause to show 100% before transitioning
            pygame.time.delay(500)
            self.state_manager.change_state('inventory')
    
    def load_assets(self):
        """Load all game assets"""
        total_stages = 3
        
        # Stage 1: Load UI images
        self.current_stage_text = self.load_stages[0]
        self.resource_manager.load_ui_images(
            LOGO_PATH, GACHA_RED_PATH, GACHA_BLUE_PATH, GACHA_YELLOW_PATH, POKEDOLLAR_ICON_PATH, RAYS_PATH
        )
        self.progress = 1 / total_stages
        pygame.display.flip()  # Update display to show progress
        
        # Stage 2: Load Pokemon sprites with progress callback
        self.current_stage_text = self.load_stages[1]
        def sprite_progress(current, total):
            base_progress = 1 / total_stages
            sprite_progress = (current / total) / total_stages
            self.progress = base_progress + sprite_progress
            if current % 10 == 0:  # Update display every 10 sprites
                self.render()
                pygame.display.flip()
        
        self.resource_manager.preload_all_sprites(sprite_progress)
        self.progress = 2 / total_stages
        pygame.display.flip()
        
        # Stage 3: Load audio
        self.current_stage_text = self.load_stages[2]
        self.audio_manager.load_game_sounds(SOUNDS_PATH)
        self.audio_manager.load_background_music_tracks(SOUNDS_PATH)
        self.progress = 1.0
        
        # Start random background music
        self.audio_manager.play_random_background_music()
        
        self.current_stage_text = self.load_stages[3]
    
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
            overlay.fill((0, 0, 0, 128))  # 50% opacity black
            self.screen.blit(overlay, (0, 0))
        else:
            # Fallback: just black background with title
            font_title = pygame.font.Font(None, 72)
            title = font_title.render("POKÉMON BLUE GACHA", True, COLOR_WHITE)
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, 200))
            self.screen.blit(title, title_rect)
        
        # Stage text
        font_stage = pygame.font.Font(None, 32)
        stage_text = font_stage.render(self.current_stage_text, True, COLOR_WHITE)
        stage_rect = stage_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 40))
        self.screen.blit(stage_text, stage_rect)
        
        # Percentage text
        font = pygame.font.Font(None, 48)
        percent_text = font.render(f"{int(self.progress * 100)}%", True, COLOR_WHITE)
        percent_rect = percent_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(percent_text, percent_rect)
        
        # Draw progress bar
        bar_width = 500
        bar_height = 30
        bar_x = (self.screen.get_width() - bar_width) // 2
        bar_y = self.screen.get_height() // 2 + 60
        
        # Background
        pygame.draw.rect(self.screen, (64, 64, 64), (bar_x, bar_y, bar_width, bar_height))
        # Progress
        progress_width = int(bar_width * self.progress)
        if progress_width > 0:
            pygame.draw.rect(self.screen, COLOR_WHITE, (bar_x, bar_y, progress_width, bar_height))
        # Border
        pygame.draw.rect(self.screen, COLOR_WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Instruction text if complete
        if self.loading_complete:
            font_small = pygame.font.Font(None, 24)
            instruction = font_small.render("Press any key to continue", True, COLOR_WHITE)
            instruction_rect = instruction.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 100))
            self.screen.blit(instruction, instruction_rect)

