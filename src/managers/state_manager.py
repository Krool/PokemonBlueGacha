"""
Game state management
"""
import pygame
from typing import Dict, Optional


class StateManager:
    """Manages game state transitions"""
    
    def __init__(self, screen, clock):
        """
        Initialize state manager
        
        Args:
            screen: pygame display surface
            clock: pygame Clock object
        """
        self.screen = screen
        self.clock = clock
        self.states: Dict[str, any] = {}
        self.current_state: Optional[any] = None
        self.current_state_name: Optional[str] = None
    
    def register_state(self, name: str, state):
        """
        Register a state with a name
        
        Args:
            name: Unique name for the state
            state: GameState instance
        """
        self.states[name] = state
        print(f"✓ Registered state: {name}")
    
    def change_state(self, name: str, **kwargs):
        """
        Switch to a different state
        
        Args:
            name: Name of state to switch to
            **kwargs: Optional parameters to pass to new state's enter method
        """
        if name not in self.states:
            raise ValueError(f"State '{name}' not registered")
        
        # Exit current state
        if self.current_state:
            self.current_state.exit()
        
        # Enter new state
        self.current_state = self.states[name]
        self.current_state_name = name
        print(f"→ Changed to state: {name}")
        self.current_state.enter(**kwargs)
    
    def handle_events(self, events):
        """
        Pass events to current state
        
        Args:
            events: List of pygame events
        """
        if self.current_state:
            self.current_state.handle_events(events)
    
    def update(self, dt):
        """
        Update current state
        
        Args:
            dt: Delta time in seconds
        """
        if self.current_state:
            self.current_state.update(dt)
    
    def render(self):
        """Render current state"""
        if self.current_state:
            self.current_state.render()

