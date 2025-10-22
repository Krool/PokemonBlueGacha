# Bug Fixes Summary

## 1. Music Randomization Trigger Fixed ✅

**Issue**: Background music was changing when clicking the currency (to add money), but should only change when clicking the "Pokédex" title.

**Files Changed**: `src/states/inventory_state.py`

**Changes**:
1. Added `self.title_rect` to store clickable area for title
2. Stored title rect when rendering: `self.title_rect = title_surface.get_rect(topleft=(title_x, title_y))`
3. Added click handler for title:
   ```python
   # Check for title click (randomize music)
   if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
       if self.title_rect and self.title_rect.collidepoint(event.pos):
           # Randomize background music if not muted
           if not self.game_data.music_muted:
               self.audio_manager.play_random_background_music()
           continue
   ```
4. Removed music randomization from currency click handler

**Result**: 
- ✅ Clicking "POKÉDEX" title → Randomizes music
- ✅ Clicking currency → Only adds money (no music change)

---

## 2. Gacha Info Popup Format Error Fixed ✅

**Issue**: Clicking the INFO button on Red/Blue/Yellow gacha machines crashed with:
```
ValueError: Unknown format code 'd' for object of type 'str'
```

**Root Cause**: `pokemon.number` is a string (e.g., "001"), but the code tried to format it as an integer with `:03d`.

**File Changed**: `src/ui/gacha_info_popup.py`

**Fix**:
```python
# Before (crashed):
name_text = f"#{pokemon.number:03d} {pokemon.name}"

# After (works):
name_text = f"#{pokemon.number} {pokemon.name}"
```

**Result**: 
- ✅ INFO button works on all Pokemon gacha machines
- ✅ Displays Pokemon numbers correctly (already padded in data)

---

## Status

✅ **Both bugs fixed!**
- Music randomization now triggered by Pokédex title click
- Gacha info popup displays correctly for all machines

The game should now run without these crashes.

