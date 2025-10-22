# Python to Web Conversion Issues

This document outlines issues found in the codebase that exist due to converting from a native Python/Pygame application to a webview program (Pygbag).

## Critical Issues

### ✅ 1. **Blocking `pygame.time.delay()` Call - FIXED**
**Location:** `src/states/loading_state.py:71`

**Status:** ✅ **FIXED** - Replaced with async timer pattern

**Solution Implemented:**
- Added `self.transition_timer` and `self.showing_complete` to track async delay
- Modified `update()` to decrement timer each frame instead of blocking
- Now yields to browser event loop during the 500ms delay

**Changes:**
```python
# Added to enter():
self.transition_timer = 0.0
self.showing_complete = False

# Replaced blocking delay with async timer in update():
if self.loading_complete:
    if self.showing_complete:
        self.transition_timer -= dt
        if self.transition_timer <= 0:
            self.state_manager.change_state('inventory')
    return
```

---

### ✅ 2. **`sys.exit()` Calls May Not Work Properly on Web - FIXED**
**Location:** `src/main.py:93, 96, 191, 203`

**Status:** ✅ **FIXED** - Added web platform checks

**Solution Implemented:**
1. Added `IS_WEB` import from config
2. Added `_show_fatal_error()` method to display errors on screen for web
3. Wrapped all `sys.exit()` calls with `if not IS_WEB:` checks
4. On web, errors are displayed on screen and exceptions are re-raised to stop initialization
5. On web quit, the function simply returns without calling sys.exit()

**Changes:**
```python
# Fatal error handling:
if not IS_WEB:
    sys.exit(1)
else:
    self._show_fatal_error(f"FATAL ERROR: {e}")
    raise  # Prevent further initialization

# Quit function:
if not IS_WEB:
    sys.exit()
# On web, just stop the running flag and let the loop exit naturally

# main() function:
if not IS_WEB:
    sys.exit(1)
else:
    print("\n[WEB] Game stopped due to critical error. Check console for details.")
    return
```

---

## Major Issues

### 3. **Synchronous CSV Loading May Cause Browser Freezing**
**Location:** `src/data/csv_loader.py` (all load functions)

**Issue:** All CSV files are loaded synchronously during initialization:
```python
with open(filepath, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    # Process all rows synchronously
```

**Problem:** In Pygbag, file I/O goes through the virtual filesystem which can be slow. Loading multiple large CSV files synchronously during initialization can cause the loading screen to appear frozen because the main loop isn't running yet.

**Current Mitigation:** The loading happens before the async main loop starts, so it's somewhat acceptable, but not ideal.

**Impact:** Medium - Longer initial load times, potential perceived freeze

**Suggestions:**
1. **Current approach is workable** - Since loading happens before entering the game loop, it's acceptable
2. **Better approach** - Load CSVs during the LoadingState with incremental updates:
   - Move CSV loading into LoadingState.load_assets()
   - Add `await asyncio.sleep(0)` calls between each CSV file load
   - Update progress bar between each file
3. **Best approach** - Preprocess CSVs into JSON during build time and load as JSON (faster parsing)

---

### 4. **Synchronous Image Loading During Preload**
**Location:** `src/managers/resource_manager.py:153-179`

**Issue:**
```python
def preload_all_sprites(self, progress_callback=None):
    for pokemon in self.pokemon_list:
        self.load_image(pokemon.image_path)  # Synchronous load
        current += 1
```

**Problem:** Loading 151 Pokemon sprites + type icons synchronously. Each `pygame.image.load()` is a blocking I/O operation that can cause stuttering.

**Current Mitigation:** There's a `pygame.display.flip()` call every 10 sprites in loading_state.py which helps.

**Impact:** Low-Medium - Loading works but could be smoother

**Suggestions:**
1. Current approach is acceptable since progress callback updates every 10 sprites
2. Could add `await asyncio.sleep(0)` in the loading state's sprite_progress callback
3. Consider lazy loading - only load sprites as needed rather than all upfront

---

## Minor Issues

### 5. **Redundant Web Platform Checks**
**Location:** `src/config.py` and `src/managers/save_manager.py`

**Issue:** Web platform detection is duplicated:
```python
# In config.py
IS_WEB = sys.platform == "emscripten"

# In save_manager.py
try:
    import sys
    IS_WEB = sys.platform == "emscripten"
except:
    IS_WEB = False
```

**Problem:** Code duplication. If save_manager.py imports from config, it should use that IS_WEB value.

**Impact:** Very Low - Just code cleanliness

**Solution:**
```python
# In save_manager.py
from config import IS_WEB
```

---

### 6. **Audio Manager Complexity**
**Location:** `src/managers/audio_manager.py`

**Issue:** The audio manager has extensive debugging code and complex web-specific workarounds:
- Verbose console logging (lines 92-172)
- Complex channel management for web
- User interaction detection logic

**Problem:** 
- Makes code harder to maintain
- Excessive console logging in production
- Some of this complexity may be unnecessary with modern Pygbag

**Impact:** Low - Functional but messy

**Suggestions:**
1. Add a DEBUG flag to control verbose logging
2. Clean up excessive console.log calls in production
3. Consider simplifying channel management if sound effects work reliably now
4. The extensive debugging was likely added during troubleshooting and could be reduced

---

### 7. **Mixed Async/Sync Patterns**
**Location:** Throughout codebase

**Issue:** The game loop is async (for web), but all internal logic is synchronous:
```python
async def run(self):
    while self.running:
        # ... synchronous operations ...
        await asyncio.sleep(0)  # Only async call
```

**Problem:** Not really a problem, but worth noting. The async is only for yielding to browser, not for actual async operations.

**Impact:** None - This is actually the correct pattern for Pygbag

**Note:** This is intentional and correct. Pygbag requires `await asyncio.sleep(0)` in the main loop to yield to the browser's event loop. Internal game logic should remain synchronous for simplicity.

---

## Issues That Were Already Fixed

### ✅ Save System - Already Converted
The save system correctly detects web platform and uses localStorage instead of file system. This is well implemented.

### ✅ Path Handling - Already Converted  
`config.py` correctly handles base paths for both desktop and web environments.

### ✅ Main Loop - Already Converted
Main loop is properly async with `await asyncio.sleep(0)` to yield to browser.

---

## Recommendations by Priority

### ✅ High Priority (COMPLETED)
1. ✅ **Replace `pygame.time.delay(500)` in loading_state.py** with async timer - **DONE**
2. ✅ **Handle `sys.exit()` calls properly** for web platform - **DONE**

### Medium Priority (Consider Fixing)
3. ✅ **Add error state** instead of crashing on fatal errors - **DONE** (added `_show_fatal_error()` method)
4. **Review and potentially simplify** audio manager complexity
5. **Add debug flag** to control verbose logging

### Low Priority (Nice to Have)
6. **Remove duplicate IS_WEB detection** in save_manager.py
7. **Consider lazy loading** for sprites instead of preloading all
8. **Add build-time CSV to JSON conversion** for faster loading

---

## Testing Checklist

After fixing issues, test these scenarios on web:

- [ ] Loading screen completes smoothly without freezing
- [ ] Game gracefully handles missing files instead of crashing
- [ ] Audio works after first user interaction
- [ ] Save/load works with localStorage
- [ ] Game can be "quit" cleanly (return to loading screen or show menu)
- [ ] No browser console errors during normal gameplay
- [ ] Tab doesn't freeze during sprite loading
- [ ] All animations are smooth (no blocking delays)

---

## Notes

The conversion to web has been mostly successful. Most web-specific concerns (localStorage, async loop, path handling) are already properly handled. The remaining issues are primarily about removing blocking calls and improving error handling for the web environment.

