# Phase 1: Project Setup & Core Infrastructure - DETAILED

## 1.1 Project Structure Setup

### Sub-steps:

#### 1.1.1 Create Directory Structure
```
PokemonBlueGacha/
├── src/                          # Source code
│   ├── __init__.py
│   ├── main.py                   # Entry point
│   ├── config.py                 # Configuration constants
│   ├── data/                     # Data management
│   │   ├── __init__.py
│   │   ├── csv_loader.py         # CSV parsing
│   │   ├── pokemon_data.py       # Pokemon data structures
│   │   ├── type_data.py          # Type data structures
│   │   └── rarity_data.py        # Rarity data structures
│   ├── managers/                 # Core managers
│   │   ├── __init__.py
│   │   ├── save_manager.py       # Save/Load
│   │   ├── resource_manager.py   # Asset loading
│   │   ├── audio_manager.py      # Sound/Music
│   │   └── state_manager.py      # Game states
│   ├── ui/                       # UI components
│   │   ├── __init__.py
│   │   ├── button.py
│   │   ├── label.py
│   │   ├── checkbox.py
│   │   ├── scrolllist.py
│   │   ├── progressbar.py
│   │   ├── popup.py
│   │   ├── pokemon_tile.py
│   │   └── utils.py              # UI utilities
│   ├── states/                   # Game states
│   │   ├── __init__.py
│   │   ├── base_state.py         # Base class
│   │   ├── loading_state.py
│   │   ├── inventory_state.py
│   │   ├── gacha_buy_state.py
│   │   ├── gacha_animation_state.py
│   │   └── gacha_outcome_state.py
│   └── logic/                    # Game logic
│       ├── __init__.py
│       ├── gacha_roller.py       # Gacha mechanics
│       ├── inventory_manager.py  # Inventory tracking
│       └── currency_manager.py   # Gold management
├── Assets/                       # All assets (already created)
│   ├── Sprites/
│   │   ├── Pokemon/
│   │   └── Types/
│   └── Sounds/
├── data/                         # CSV files (already created)
│   ├── pokemon_gen1.csv
│   ├── pokemon_types.csv
│   └── rarity_drop_weights.csv
├── saves/                        # Save files (created at runtime)
│   └── player_save.json
├── requirements.txt
└── README.md
```

#### 1.1.2 Create requirements.txt
```
pygame==2.5.2
```

#### 1.1.3 Create config.py with constants
```python
# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (128, 128, 128)

# File paths
POKEMON_CSV = "pokemon_gen1.csv"
TYPES_CSV = "pokemon_types.csv"
RARITY_CSV = "rarity_drop_weights.csv"
SAVE_FILE = "saves/player_save.json"

# Asset paths
SPRITES_PATH = "Assets/Sprites/Pokemon/"
TYPES_PATH = "Assets/Sprites/Types/"
SOUNDS_PATH = "Assets/Sounds/"
LOGO_PATH = "Assets/logo.png"
GACHA_PATH = "Assets/gacha.png"

# Game balance
STARTING_GOLD = 0
GOLD_CHEAT_AMOUNT = 10000
SINGLE_PULL_COST = 1000
TEN_PULL_COST = 9000
```

---

## 1.2 Data Loading System

### 1.2.1 Create Pokemon Data Structure (pokemon_data.py)

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Pokemon:
    number: str          # "001"
    name: str            # "Bulbasaur"
    type1: str           # "Grass"
    type2: Optional[str] # "Poison" or None
    rarity: str          # "Uncommon"
    weight: int          # 1
    image_path: str      # "Sprites/Pokemon/001_Bulbasaur.png"
    
    def get_pokedex_num(self) -> int:
        """Returns numeric Pokédex number"""
        return int(self.number)
```

### 1.2.2 Create Type Data Structure (type_data.py)

```python
from dataclasses import dataclass

@dataclass
class PokemonType:
    name: str        # "Fire"
    image_path: str  # "Sprites/Types/Fire.png"
    color_hex: str   # "#F08030"
    
    def get_color_rgb(self) -> tuple:
        """Convert hex to RGB tuple"""
        hex_color = self.color_hex.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
```

### 1.2.3 Create Rarity Data Structure (rarity_data.py)

```python
from dataclasses import dataclass

@dataclass
class Rarity:
    name: str         # "Legendary"
    drop_weight: int  # 1
    color_hex: str    # "#FF8000"
    
    def get_color_rgb(self) -> tuple:
        """Convert hex to RGB tuple"""
        hex_color = self.color_hex.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
```

### 1.2.4 Create CSV Loader (csv_loader.py)

```python
import csv
from typing import List, Dict
from .pokemon_data import Pokemon
from .type_data import PokemonType
from .rarity_data import Rarity

class CSVLoader:
    @staticmethod
    def load_pokemon(filepath: str) -> List[Pokemon]:
        """Load all Pokémon from CSV"""
        pokemon_list = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pokemon = Pokemon(
                    number=row['Number'],
                    name=row['Name'],
                    type1=row['Type1'],
                    type2=row['Type2'] if row['Type2'] else None,
                    rarity=row['Rarity'],
                    weight=int(row['Weight']),
                    image_path=row['Image']
                )
                pokemon_list.append(pokemon)
        return pokemon_list
    
    @staticmethod
    def load_types(filepath: str) -> Dict[str, PokemonType]:
        """Load all types from CSV, return dict keyed by name"""
        types_dict = {}
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                poke_type = PokemonType(
                    name=row['Type'],
                    image_path=row['Image'],
                    color_hex=row['Color']
                )
                types_dict[poke_type.name] = poke_type
        return types_dict
    
    @staticmethod
    def load_rarities(filepath: str) -> Dict[str, Rarity]:
        """Load all rarities from CSV, return dict keyed by name"""
        rarities_dict = {}
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rarity = Rarity(
                    name=row['Rarity'],
                    drop_weight=int(row['Drop_Weight']),
                    color_hex=row['Color']
                )
                rarities_dict[rarity.name] = rarity
        return rarities_dict
```

### 1.2.5 Create Data Validation

```python
def validate_data_integrity():
    """Ensure all data loaded correctly and references are valid"""
    # Check all Pokémon have valid types
    # Check all Pokémon have valid rarities
    # Check all image paths exist
    # Log any issues
```

---

## 1.3 Save System

### 1.3.1 Design Save File Structure

```json
{
    "version": "1.0",
    "gold": 15000,
    "pokemon_owned": {
        "001": 3,
        "025": 1,
        "150": 1
    },
    "newly_acquired": [
        "150"
    ],
    "stats": {
        "total_pulls": 100,
        "total_spent": 95000
    }
}
```

### 1.3.2 Create SaveManager Class (save_manager.py)

```python
import json
import os
from pathlib import Path
from typing import Dict

class SaveManager:
    def __init__(self, save_path: str):
        self.save_path = save_path
        self.ensure_save_directory()
    
    def ensure_save_directory(self):
        """Create saves directory if it doesn't exist"""
        Path(self.save_path).parent.mkdir(parents=True, exist_ok=True)
    
    def save_game(self, gold: int, pokemon_owned: Dict[str, int], 
                  newly_acquired: list, stats: dict) -> bool:
        """Save game state to JSON"""
        save_data = {
            "version": "1.0",
            "gold": gold,
            "pokemon_owned": pokemon_owned,
            "newly_acquired": newly_acquired,
            "stats": stats
        }
        
        try:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Save failed: {e}")
            return False
    
    def load_game(self) -> dict:
        """Load game state from JSON, return default if not exists"""
        if not os.path.exists(self.save_path):
            return self.get_default_save()
        
        try:
            with open(self.save_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Load failed: {e}, using default save")
            return self.get_default_save()
    
    def get_default_save(self) -> dict:
        """Return default save for new players"""
        return {
            "version": "1.0",
            "gold": 0,
            "pokemon_owned": {},
            "newly_acquired": [],
            "stats": {
                "total_pulls": 0,
                "total_spent": 0
            }
        }
    
    def delete_save(self) -> bool:
        """Delete save file (for reset)"""
        try:
            if os.path.exists(self.save_path):
                os.remove(self.save_path)
            return True
        except Exception as e:
            print(f"Delete failed: {e}")
            return False
```

---

## 1.4 Game State Manager

### 1.4.1 Create Base GameState Class (base_state.py)

```python
import pygame
from abc import ABC, abstractmethod

class GameState(ABC):
    def __init__(self, manager):
        self.manager = manager  # Reference to StateManager
        self.screen = manager.screen
        self.clock = manager.clock
    
    @abstractmethod
    def enter(self):
        """Called when entering this state"""
        pass
    
    @abstractmethod
    def exit(self):
        """Called when exiting this state"""
        pass
    
    @abstractmethod
    def handle_events(self, events):
        """Handle pygame events"""
        pass
    
    @abstractmethod
    def update(self, dt):
        """Update state logic (dt = delta time)"""
        pass
    
    @abstractmethod
    def render(self):
        """Render state to screen"""
        pass
```

### 1.4.2 Create StateManager Class (state_manager.py)

```python
import pygame
from typing import Dict, Optional

class StateManager:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.states: Dict[str, GameState] = {}
        self.current_state: Optional[GameState] = None
        self.current_state_name: Optional[str] = None
    
    def register_state(self, name: str, state: GameState):
        """Register a state with a name"""
        self.states[name] = state
    
    def change_state(self, name: str, **kwargs):
        """Switch to a different state"""
        if name not in self.states:
            raise ValueError(f"State '{name}' not registered")
        
        # Exit current state
        if self.current_state:
            self.current_state.exit()
        
        # Enter new state
        self.current_state = self.states[name]
        self.current_state_name = name
        self.current_state.enter(**kwargs)
    
    def handle_events(self, events):
        """Pass events to current state"""
        if self.current_state:
            self.current_state.handle_events(events)
    
    def update(self, dt):
        """Update current state"""
        if self.current_state:
            self.current_state.update(dt)
    
    def render(self):
        """Render current state"""
        if self.current_state:
            self.current_state.render()
```

### 1.4.3 Create Main Game Loop (main.py)

```python
import pygame
import sys
from config import *
from managers.state_manager import StateManager
from managers.resource_manager import ResourceManager
from managers.save_manager import SaveManager
from managers.audio_manager import AudioManager
from data.csv_loader import CSVLoader

# Import all states
from states.loading_state import LoadingState
from states.inventory_state import InventoryState
from states.gacha_buy_state import GachaBuyState
from states.gacha_animation_state import GachaAnimationState
from states.gacha_outcome_state import GachaOutcomeState

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pokémon Blue Gacha")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize managers
        self.save_manager = SaveManager(SAVE_FILE)
        self.resource_manager = ResourceManager()
        self.audio_manager = AudioManager()
        
        # Load game data
        self.load_game_data()
        
        # Create state manager
        self.state_manager = StateManager(self.screen, self.clock)
        self.register_states()
        
        # Start with loading state
        self.state_manager.change_state('loading')
    
    def load_game_data(self):
        """Load all CSV data"""
        self.pokemon_list = CSVLoader.load_pokemon(POKEMON_CSV)
        self.types_dict = CSVLoader.load_types(TYPES_CSV)
        self.rarities_dict = CSVLoader.load_rarities(RARITY_CSV)
        
        # Store in resource manager for global access
        self.resource_manager.pokemon_list = self.pokemon_list
        self.resource_manager.types_dict = self.types_dict
        self.resource_manager.rarities_dict = self.rarities_dict
    
    def register_states(self):
        """Register all game states"""
        self.state_manager.register_state('loading', 
            LoadingState(self.state_manager, self.resource_manager, self.audio_manager))
        self.state_manager.register_state('inventory', 
            InventoryState(self.state_manager, self.resource_manager, self.save_manager))
        self.state_manager.register_state('gacha_buy', 
            GachaBuyState(self.state_manager, self.resource_manager, self.save_manager))
        self.state_manager.register_state('gacha_animation', 
            GachaAnimationState(self.state_manager, self.resource_manager, self.audio_manager))
        self.state_manager.register_state('gacha_outcome', 
            GachaOutcomeState(self.state_manager, self.resource_manager, self.save_manager))
    
    def run(self):
        """Main game loop"""
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
        
        self.quit()
    
    def quit(self):
        """Clean shutdown"""
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
```

---

## Phase 1 Completion Checklist

- [ ] Directory structure created
- [ ] requirements.txt created
- [ ] config.py with all constants
- [ ] Pokemon data structure
- [ ] Type data structure
- [ ] Rarity data structure
- [ ] CSV Loader implemented
- [ ] Data validation function
- [ ] SaveManager class complete
- [ ] Save file structure tested
- [ ] Base GameState class
- [ ] StateManager class
- [ ] Main game loop
- [ ] All imports working
- [ ] Can run and see black screen

**Phase 1 should result in a runnable application that switches to a blank Loading state.**

