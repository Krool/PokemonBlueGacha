"""
Save/Load game state to JSON
"""
import json
import os
from pathlib import Path
from typing import Dict

# Detect web platform for localStorage
try:
    import sys
    IS_WEB = sys.platform == "emscripten"
except:
    IS_WEB = False

# Check for localStorage availability on web
if IS_WEB:
    try:
        from platform import window
        HAS_LOCALSTORAGE = hasattr(window, 'localStorage')
    except:
        HAS_LOCALSTORAGE = False
else:
    HAS_LOCALSTORAGE = False


class SaveManager:
    """Handles saving and loading game progress"""
    
    def __init__(self, save_path: str):
        self.save_path = save_path
        self.save_key = "pokemon_blue_gacha_save"  # localStorage key for web
        if not IS_WEB:
            self.ensure_save_directory()
        
        print(f"SaveManager initialized:")
        print(f"  IS_WEB: {IS_WEB}")
        print(f"  HAS_LOCALSTORAGE: {HAS_LOCALSTORAGE}")
        print(f"  Save path: {self.save_path}")
    
    def ensure_save_directory(self):
        """Create saves directory if it doesn't exist"""
        Path(self.save_path).parent.mkdir(parents=True, exist_ok=True)
    
    def save_game(self, gold: int, pokemon_owned: Dict[str, int], items_owned: Dict[str, int],
                  newly_acquired: list, newly_acquired_items: list, stats: dict, 
                  collection_complete_sound_played: bool = False, 
                  music_muted: bool = False) -> bool:
        """
        Save game state to JSON
        
        Args:
            gold: Current gold balance
            pokemon_owned: Dict mapping pokemon number to count
            items_owned: Dict mapping item number to count
            newly_acquired: List of pokemon numbers newly acquired
            newly_acquired_items: List of item numbers newly acquired
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
            "items_owned": items_owned,
            "newly_acquired": newly_acquired,
            "newly_acquired_items": newly_acquired_items,
            "stats": stats,
            "collection_complete_sound_played": collection_complete_sound_played,
            "music_muted": music_muted
        }
        
        try:
            if IS_WEB and HAS_LOCALSTORAGE:
                # Use localStorage for web (more reliable than file system)
                from platform import window
                json_str = json.dumps(save_data)
                window.localStorage.setItem(self.save_key, json_str)
                print(f"Saved to localStorage (Gold: {gold}, Pokemon: {len(pokemon_owned)}, Items: {len(items_owned)})")
                return True
            else:
                # Use file system for desktop
                with open(self.save_path, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, indent=2)
                print(f"Saved to {self.save_path}")
                return True
        except Exception as e:
            print(f"Save failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def load_game(self) -> dict:
        """
        Load game state from JSON
        
        Returns:
            Dictionary with save data, or default save if not exists
        """
        try:
            if IS_WEB and HAS_LOCALSTORAGE:
                # Load from localStorage for web
                from platform import window
                json_str = window.localStorage.getItem(self.save_key)
                if json_str and json_str != "null":
                    save_data = json.loads(json_str)
                    print(f"Loaded from localStorage (Gold: {save_data.get('gold', 0)}, Pokemon: {len(save_data.get('pokemon_owned', {}))})")
                    return save_data
                else:
                    print("No save in localStorage, starting new game")
                    return self.get_default_save()
            else:
                # Load from file system for desktop
                if not os.path.exists(self.save_path):
                    print("No save file found, starting new game")
                    return self.get_default_save()
                
                with open(self.save_path, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                print(f"Loaded from {self.save_path}")
                return save_data
        except Exception as e:
            print(f"Load failed: {e}, using default save")
            import traceback
            traceback.print_exc()
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
            "items_owned": {},
            "newly_acquired": [],
            "newly_acquired_items": [],
            "stats": {
                "total_pulls": 0,
                "total_spent": 0,
                "pulls_by_version": {"Red": 0, "Blue": 0, "Yellow": 0, "Items": 0}
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
            if IS_WEB and HAS_LOCALSTORAGE:
                # Delete from localStorage for web
                from platform import window
                window.localStorage.removeItem(self.save_key)
                print("Save deleted from localStorage")
                return True
            else:
                # Delete from file system for desktop
                if os.path.exists(self.save_path):
                    os.remove(self.save_path)
                    print("Save file deleted")
                return True
        except Exception as e:
            print(f"Delete failed: {e}")
            return False

