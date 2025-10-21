"""
Base class for all game states
"""
import pygame
from abc import ABC, abstractmethod


class GameState(ABC):
    """Base class for all game states"""
    
    def __init__(self, state_manager, game_data, resource_manager, audio_manager, font_manager=None, gacha_system=None):
        """
        Initialize game state
        
        Args:
            state_manager: StateManager instance
            game_data: GameData instance
            resource_manager: ResourceManager instance
            audio_manager: AudioManager instance
            font_manager: FontManager instance (optional)
            gacha_system: GachaSystem instance (optional)
        """
        self.state_manager = state_manager
        self.game_data = game_data
        self.resource_manager = resource_manager
        self.audio_manager = audio_manager
        self.font_manager = font_manager
        self.gacha_system = gacha_system
        self.screen = state_manager.screen
        self.clock = state_manager.clock
    
    @abstractmethod
    def enter(self, **kwargs):
        """
        Called when entering this state
        
        Args:
            **kwargs: Optional parameters passed during state change
        """
        pass
    
    @abstractmethod
    def exit(self):
        """Called when exiting this state"""
        pass
    
    @abstractmethod
    def handle_events(self, events):
        """
        Handle pygame events
        
        Args:
            events: List of pygame events
        """
        pass
    
    @abstractmethod
    def update(self, dt):
        """
        Update state logic
        
        Args:
            dt: Delta time in seconds since last frame
        """
        pass
    
    @abstractmethod
    def render(self):
        """Render state to screen"""
        pass

