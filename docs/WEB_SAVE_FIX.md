# Web Save System Issue & Fix

## 🐛 Problem

State doesn't persist between page refreshes in the web version.

## 🔍 Root Cause

The save system works correctly, but there's a timing/sync issue with how Pygbag maps Python file I/O to browser IndexedDB storage.

### Current Save Configuration:
```python
# config.py line 39
SAVE_FILE = os.path.join(BASE_PATH, "saves/player_save.json") if not IS_WEB else "player_save.json"
```

### Issues:
1. **Async Storage**: IndexedDB is asynchronous, but Python `open()`/`json.dump()` are synchronous
2. **Timing**: Pygbag needs time to sync file writes to IndexedDB
3. **Directory Structure**: The `saves/` directory might not be properly created in virtual filesystem

## ✅ Solution

### Option 1: Use localStorage Instead (Recommended for Web)

Pygbag provides direct localStorage access which is synchronous and more reliable for web games.

**Add to `save_manager.py`:**

```python
import json
import os
from pathlib import Path
from typing import Dict
from config import IS_WEB

if IS_WEB:
    import platform
    # Check if we can use localStorage
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
        self.save_key = "pokemon_blue_gacha_save"  # localStorage key
        if not IS_WEB:
            self.ensure_save_directory()
    
    def save_game(self, gold: int, pokemon_owned: Dict[str, int], items_owned: Dict[str, int],
                  newly_acquired: list, newly_acquired_items: list, stats: dict, 
                  collection_complete_sound_played: bool = False, 
                  music_muted: bool = False) -> bool:
        """Save game state"""
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
                # Use localStorage for web
                from platform import window
                json_str = json.dumps(save_data)
                window.localStorage.setItem(self.save_key, json_str)
                print(f"✓ Saved to localStorage")
            else:
                # Use file system for desktop
                with open(self.save_path, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, indent=2)
                print(f"✓ Saved to {self.save_path}")
            return True
        except Exception as e:
            print(f"Save failed: {e}")
            return False
    
    def load_game(self) -> dict:
        """Load game state"""
        try:
            if IS_WEB and HAS_LOCALSTORAGE:
                # Load from localStorage for web
                from platform import window
                json_str = window.localStorage.getItem(self.save_key)
                if json_str:
                    save_data = json.loads(json_str)
                    print(f"✓ Loaded from localStorage")
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
                print(f"✓ Loaded from {self.save_path}")
                return save_data
        except Exception as e:
            print(f"Load failed: {e}, using default save")
            return self.get_default_save()
```

### Option 2: Ensure Async Flush (Simpler, Keep File System)

If you want to keep using the file system approach, add an async flush:

```python
# In save_manager.py
async def save_game_async(self, ...):
    """Async version for web"""
    # ... save code ...
    if IS_WEB:
        import asyncio
        await asyncio.sleep(0)  # Let Pygbag sync to IndexedDB
    return True
```

### Option 3: Add Debug Logging

First, let's see if saves are actually working by adding better logging:

```python
def save_game(self, ...):
    # ... existing code ...
    try:
        with open(self.save_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2)
        print(f"✓ Save successful! Path: {self.save_path}")
        print(f"  Gold: {gold}, Pokémon: {len(pokemon_owned)}, Items: {len(items_owned)}")
        return True
    except Exception as e:
        print(f"✗ Save failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def load_game(self):
    print(f"Attempting to load from: {self.save_path}")
    print(f"File exists: {os.path.exists(self.save_path)}")
    # ... rest of code ...
```

## 🧪 Testing the Fix

### Check Browser Console

After playing and refreshing, check the browser console (F12) for:

```
✓ Save successful! Path: player_save.json
  Gold: 10000, Pokémon: 5, Items: 3
```

Then after refresh:
```
Attempting to load from: player_save.json
File exists: True
✓ Loaded from player_save.json
```

### Check Browser Storage

1. Open DevTools (F12)
2. Go to **Application** tab (Chrome) or **Storage** tab (Firefox)
3. Look under **IndexedDB** for Pygbag entries
4. OR look under **Local Storage** if using Option 1

## 📋 Recommended Implementation: Option 1 (localStorage)

**Pros:**
- ✅ Synchronous (no timing issues)
- ✅ More reliable for web games
- ✅ Faster (no filesystem overhead)
- ✅ Standard web storage approach

**Cons:**
- ⚠️ Requires checking for localStorage availability
- ⚠️ Different code paths for web vs desktop

## 🎯 Quick Fix Right Now

Add this to save_manager.py to at least see what's happening:

```python
def save_game(self, ...):
    save_data = {...}
    
    try:
        print(f"💾 Attempting save to: {self.save_path}")
        with open(self.save_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2)
        print(f"✓ Save written! Gold: {gold}, Pokémon: {len(pokemon_owned)}")
        
        # Verify it was written
        if os.path.exists(self.save_path):
            print(f"✓ File verified exists")
        else:
            print(f"⚠️ Warning: File doesn't exist after write!")
        
        return True
    except Exception as e:
        print(f"✗ Save ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
```

This will help diagnose whether:
1. Saves are being attempted
2. Saves are succeeding
3. Files exist after save
4. Errors are occurring

## 🔧 Implementation Priority

1. **Immediate**: Add debug logging (see what's happening)
2. **Short-term**: Implement localStorage (Option 1) - most reliable
3. **Long-term**: Consider hybrid approach (localStorage with file fallback)

## 📞 Pygbag Specific Notes

Pygbag automatically syncs Python file I/O to IndexedDB, but:
- Sync happens asynchronously
- Page refresh might happen before sync completes
- localStorage is more reliable for quick save/load cycles
- IndexedDB persists across sessions (when it works)

## 🚀 Deploy Fix

After implementing:
1. Test locally: `pygbag src/main.py`
2. Test in browser console
3. Rebuild: `pygbag --build src/main.py`
4. Redeploy: `.\deploy.bat`
5. Test live site
6. Verify saves persist after refresh


