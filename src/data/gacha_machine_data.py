"""Data class for Gacha Machine definitions."""

class GachaMachine:
    """Represents a gacha machine (Red, Blue, or Yellow version)."""
    
    def __init__(self, name: str, version: str, cost_single: int, cost_10pull: int, description: str):
        self.name = name
        self.version = version  # "Red", "Blue", or "Yellow"
        self.cost_single = cost_single
        self.cost_10pull = cost_10pull
        self.description = description
    
    def __repr__(self):
        return f"GachaMachine({self.name}, {self.version}, Single: {self.cost_single}, 10-Pull: {self.cost_10pull})"

