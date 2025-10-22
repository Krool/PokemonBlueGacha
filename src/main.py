"""
Pokémon Blue Gacha - Main Entry Point
"""
import pygame
import sys
import asyncio
from config import *
from config import IS_WEB
from managers.state_manager import StateManager
from managers.resource_manager import ResourceManager
from managers.save_manager import SaveManager
from managers.game_data import GameData
from managers.audio_manager import AudioManager
from managers.font_manager import FontManager
from data.csv_loader import CSVLoader, CSVLoadError
from logic.gacha_logic import GachaSystem

# Import states
from states.loading_state import LoadingState
from states.inventory_state import InventoryState
from states.gacha_buy_state import GachaBuyState
from states.gacha_animation_state import GachaAnimationState
from states.gacha_outcome_state import GachaOutcomeState


class Game:
    """Main game class"""
    
    def __init__(self):
        """Initialize game"""
        print("=" * 60)
        print("POKÉMON BLUE GACHA - Initializing...")
        print("=" * 60)
        
        # Initialize pygame
        pygame.init()
        # Note: pygame.mixer will be initialized by AudioManager with proper settings
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pokémon Blue Gacha")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize managers
        print("\nInitializing managers...")
        self.save_manager = SaveManager(SAVE_FILE)
        self.game_data = GameData(self.save_manager)
        self.resource_manager = ResourceManager()
        self.audio_manager = AudioManager()
        self.font_manager = FontManager(TITLE_FONT_PATH, BODY_FONT_PATH)
        
        # Load game data
        self.load_game_data()
        
        # Initialize gacha system
        self.gacha_system = GachaSystem(
            self.resource_manager.pokemon_list,
            self.resource_manager.rarities_dict
        )
        
        # Create state manager
        self.state_manager = StateManager(self.screen, self.clock)
        self.register_states()
        
        print("\n" + "=" * 60)
        print("[OK] Initialization complete!")
        print("=" * 60 + "\n")
        
        # Start with loading state
        self.state_manager.change_state('loading')
    
    def _show_fatal_error(self, message: str):
        """
        Display a fatal error message on screen (for web)
        
        Args:
            message: Error message to display
        """
        print(f"\n{'='*60}")
        print(f"FATAL ERROR - GAME CANNOT START")
        print(f"{'='*60}")
        print(message)
        print(f"{'='*60}\n")
        
        # Display error on screen
        self.screen.fill(COLOR_BLACK)
        
        # Error title
        font_title = pygame.font.Font(None, 48)
        title_surface = font_title.render("FATAL ERROR", True, (255, 0, 0))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(title_surface, title_rect)
        
        # Error message (split into lines if too long)
        font_body = pygame.font.Font(None, 24)
        y_offset = SCREEN_HEIGHT // 2
        max_width = SCREEN_WIDTH - 100
        
        words = message.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font_body.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        for line in lines[:5]:  # Show max 5 lines
            text_surface = font_body.render(line, True, COLOR_WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 30
        
        # Instruction
        instruction = font_body.render("Check console for details", True, (200, 200, 200))
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()
    
    def load_game_data(self):
        """Load all CSV data"""
        print("\nLoading game data...")
        
        try:
            # Load CSVs
            self.resource_manager.pokemon_list = CSVLoader.load_pokemon(POKEMON_CSV)
            self.resource_manager.types_dict = CSVLoader.load_types(TYPES_CSV)
            self.resource_manager.rarities_dict = CSVLoader.load_rarities(RARITY_CSV)
            self.resource_manager.gacha_machines_dict = CSVLoader.load_gacha_machines(GACHA_MACHINES_CSV)
            self.resource_manager.items_list = CSVLoader.load_items(ITEMS_CSV)
            
            # Validate data integrity
            CSVLoader.validate_data_integrity(
                self.resource_manager.pokemon_list,
                self.resource_manager.types_dict,
                self.resource_manager.rarities_dict
            )
            
        except CSVLoadError as e:
            print(f"\n[ERROR] FATAL ERROR: {e}")
            print("Cannot continue without valid game data.")
            if not IS_WEB:
                sys.exit(1)
            else:
                # On web, display error and prevent game from starting
                self._show_fatal_error(f"FATAL ERROR: {e}")
                raise  # Re-raise to prevent further initialization
        except Exception as e:
            print(f"\n[ERROR] UNEXPECTED ERROR: {e}")
            if not IS_WEB:
                sys.exit(1)
            else:
                self._show_fatal_error(f"UNEXPECTED ERROR: {e}")
                raise
    
    def register_states(self):
        """Register all game states"""
        print("\nRegistering game states...")
        
        # Create state instances
        loading_state = LoadingState(
            self.state_manager, 
            self.game_data, 
            self.resource_manager, 
            self.audio_manager,
            self.font_manager
        )
        
        inventory_state = InventoryState(
            self.state_manager, 
            self.game_data, 
            self.resource_manager, 
            self.audio_manager,
            self.font_manager
        )
        
        gacha_buy_state = GachaBuyState(
            self.state_manager,
            self.game_data,
            self.resource_manager,
            self.audio_manager,
            self.font_manager,
            self.gacha_system
        )
        
        gacha_animation_state = GachaAnimationState(
            self.state_manager,
            self.game_data,
            self.resource_manager,
            self.audio_manager,
            self.font_manager,
            self.gacha_system
        )
        
        gacha_outcome_state = GachaOutcomeState(
            self.state_manager,
            self.game_data,
            self.resource_manager,
            self.audio_manager,
            self.font_manager,
            self.gacha_system
        )
        
        # Register states
        self.state_manager.register_state('loading', loading_state)
        self.state_manager.register_state('inventory', inventory_state)
        self.state_manager.register_state('gacha_buy', gacha_buy_state)
        self.state_manager.register_state('gacha_animation', gacha_animation_state)
        self.state_manager.register_state('gacha_outcome', gacha_outcome_state)
    
    async def run(self):
        """Main game loop - async for web compatibility"""
        print("\nStarting main game loop...\n")
        
        while self.running:
            try:
                dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
                
                # Handle events
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.running = False
                
                self.state_manager.handle_events(events)
                
                # Update
                self.state_manager.update(dt)
                
                # Render
                self.screen.fill(COLOR_BLACK)
                self.state_manager.render()
                pygame.display.flip()
                
            except Exception as e:
                # Silently handle all exceptions on web (prevents Pygbag error popups)
                # Print to console for debugging but don't let it crash the game
                if IS_WEB:
                    # Only log unique errors to avoid console spam
                    error_msg = str(e)
                    if "fetching process" in error_msg or "media resource" in error_msg:
                        pass  # Silently ignore audio errors
                    else:
                        print(f"[WARN] Game loop error (suppressed): {e}")
                else:
                    # On desktop, re-raise to catch actual bugs
                    raise
            
            # Yield to browser (crucial for Pygbag)
            await asyncio.sleep(0)
        
        self.quit()
    
    def quit(self):
        """Clean shutdown"""
        print("\nShutting down...")
        
        # Save game before quitting
        print("Saving game...")
        self.game_data.save()
        
        pygame.quit()
        print("[OK] Goodbye!")
        
        # Only call sys.exit() on desktop, not on web
        if not IS_WEB:
            sys.exit()
        # On web, just stop the running flag and let the loop exit naturally


async def main():
    """Entry point - async for web compatibility"""
    try:
        game = Game()
        await game.run()
    except Exception as e:
        print(f"\n[ERROR] CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        # Only call sys.exit() on desktop
        if not IS_WEB:
            sys.exit(1)
        else:
            # On web, just let the function end naturally
            # The browser will show the error in console
            print("\n[WEB] Game stopped due to critical error. Check console for details.")
            return


if __name__ == "__main__":
    asyncio.run(main())

