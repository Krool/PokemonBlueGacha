"""
Save/Load game state to JSON
"""
import json
import os
from pathlib import Path
from typing import Dict


class SaveManager:
    """Handles saving and loading game progress"""
    
    def __init__(self, save_path: str):
        self.save_path = save_path
        self.ensure_save_directory()
    
    def ensure_save_directory(self):
        """Create saves directory if it doesn't exist"""
        Path(self.save_path).parent.mkdir(parents=True, exist_ok=True)
    
    def save_game(self, gold: int, pokemon_owned: Dict[str, int], 
                  newly_acquired: list, stats: dict, collection_complete_sound_played: bool = False, 
                  music_muted: bool = False) -> bool:
        """
        Save game state to JSON
        
        Args:
            gold: Current gold balance
            pokemon_owned: Dict mapping pokemon number to count
            newly_acquired: List of pokemon numbers newly acquired
            stats: Game statistics
            collection_complete_sound_played: Whether the collection complete sound has been played
            music_muted: Whether background music is muted
            
        Returns:
            True if save successful, False otherwise
        """
        save_data = {
            "version": "1.0",
            "gold": gold,
            "pokemon_owned": pokemon_owned,
            "newly_acquired": newly_acquired,
            "stats": stats,
            "collection_complete_sound_played": collection_complete_sound_played,
            "music_muted": music_muted
        }
        
        try:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Save failed: {e}")
            return False
    
    def load_game(self) -> dict:
        """
        Load game state from JSON
        
        Returns:
            Dictionary with save data, or default save if not exists
        """
        if not os.path.exists(self.save_path):
            print("No save file found, starting new game")
            return self.get_default_save()
        
        try:
            with open(self.save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            print(f"✓ Loaded save file")
            return save_data
        except Exception as e:
            print(f"Load failed: {e}, using default save")
            return self.get_default_save()
    
    def get_default_save(self) -> dict:
        """
        Return default save for new players
        
        Returns:
            Dictionary with default game state
        """
        return {
            "version": "1.0",
            "gold": 0,
            "pokemon_owned": {},
            "newly_acquired": [],
            "stats": {
                "total_pulls": 0,
                "total_spent": 0
            },
            "collection_complete_sound_played": False,
            "music_muted": False
        }
    
    def delete_save(self) -> bool:
        """
        Delete save file (for reset)
        
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            if os.path.exists(self.save_path):
                os.remove(self.save_path)
                print("Save file deleted")
            return True
        except Exception as e:
            print(f"Delete failed: {e}")
            return False

