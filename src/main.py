"""
Pokémon Blue Gacha - Main Entry Point
"""
import pygame
import sys
import asyncio
from config import *
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
        print("✓ Initialization complete!")
        print("=" * 60 + "\n")
        
        # Start with loading state
        self.state_manager.change_state('loading')
    
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
            print(f"\n✗ FATAL ERROR: {e}")
            print("Cannot continue without valid game data.")
            sys.exit(1)
        except Exception as e:
            print(f"\n✗ UNEXPECTED ERROR: {e}")
            sys.exit(1)
    
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
        print("✓ Goodbye!")
        sys.exit()


async def main():
    """Entry point - async for web compatibility"""
    try:
        game = Game()
        await game.run()
    except Exception as e:
        print(f"\n✗ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

