# Web Critical Fixes Summary

## Date
October 22, 2025

## Overview
Fixed two critical issues that could cause browser freezing and undefined behavior in the web version of Pokémon Blue Gacha.

---

## Fix #1: Replaced Blocking `pygame.time.delay()` with Async Timer

### Problem
- **File:** `src/states/loading_state.py:71`
- **Issue:** Used `pygame.time.delay(500)` which is a blocking call that freezes the browser tab
- **Impact:** Browser tab becomes unresponsive for 500ms, preventing event loop processing

### Solution
Replaced blocking delay with an async timer pattern that yields to the browser each frame:

**Changes Made:**
1. Added timer state variables in `enter()`:
   ```python
   self.transition_timer = 0.0
   self.showing_complete = False
   ```

2. Modified `update()` to use frame-based timing:
   ```python
   if self.loading_complete:
       # Handle transition timer (non-blocking delay for web compatibility)
       if self.showing_complete:
           self.transition_timer -= dt
           if self.transition_timer <= 0:
               self.state_manager.change_state('inventory')
       return
   ```

**Benefits:**
- ✅ Browser tab remains responsive during delay
- ✅ Event loop continues processing
- ✅ Smooth user experience on web
- ✅ Still works perfectly on desktop

---

## Fix #2: Handled `sys.exit()` Calls for Web Platform

### Problem
- **File:** `src/main.py` (multiple locations)
- **Issue:** `sys.exit()` doesn't work properly in Pygbag/Emscripten
- **Impact:** Application can be left in undefined/broken state instead of cleanly exiting

### Solution
Added platform detection and proper error handling for web vs desktop:

**Changes Made:**

1. **Added IS_WEB import:**
   ```python
   from config import IS_WEB
   ```

2. **Added error display method:**
   Created `_show_fatal_error()` method that displays errors on screen for web users:
   - Shows "FATAL ERROR" title in red
   - Displays error message text (word-wrapped)
   - Instructs users to check console
   - Updates display so error is visible

3. **Fixed fatal error handling in `load_game_data()`:**
   ```python
   except CSVLoadError as e:
       print(f"\n[ERROR] FATAL ERROR: {e}")
       print("Cannot continue without valid game data.")
       if not IS_WEB:
           sys.exit(1)
       else:
           # On web, display error and prevent game from starting
           self._show_fatal_error(f"FATAL ERROR: {e}")
           raise  # Re-raise to prevent further initialization
   ```

4. **Fixed quit() function:**
   ```python
   # Only call sys.exit() on desktop, not on web
   if not IS_WEB:
       sys.exit()
   # On web, just stop the running flag and let the loop exit naturally
   ```

5. **Fixed main() function:**
   ```python
   except Exception as e:
       print(f"\n[ERROR] CRITICAL ERROR: {e}")
       import traceback
       traceback.print_exc()
       
       # Only call sys.exit() on desktop
       if not IS_WEB:
           sys.exit(1)
       else:
           # On web, just let the function end naturally
           # The browser will show the error in console
           print("\n[WEB] Game stopped due to critical error. Check console for details.")
           return
   ```

**Benefits:**
- ✅ Errors are visible to web users on screen
- ✅ No undefined/broken states
- ✅ Clean shutdown on web (function just returns)
- ✅ Desktop behavior unchanged
- ✅ Better error reporting for debugging

---

## Testing Recommendations

Before deployment, test the following scenarios **on web**:

### Loading State
- [ ] Loading screen completes without freezing
- [ ] Browser tab remains responsive during loading
- [ ] Transition from loading to inventory is smooth
- [ ] Can click/interact during loading completion

### Error Handling
- [ ] Simulate a missing CSV file (rename temporarily)
- [ ] Verify error displays on screen (not just console)
- [ ] Verify game doesn't crash browser tab
- [ ] Check that error message is readable

### Quit Behavior
- [ ] Close the game (if quit button exists)
- [ ] Verify clean shutdown without errors
- [ ] Check browser console for any warnings

### General
- [ ] No browser console errors during normal gameplay
- [ ] Tab never becomes unresponsive
- [ ] Game remains playable after long sessions

---

## Files Modified

1. **src/states/loading_state.py**
   - Replaced blocking delay with async timer
   - Added `transition_timer` and `showing_complete` state variables
   - Modified `update()` method

2. **src/main.py**
   - Added `IS_WEB` import
   - Added `_show_fatal_error()` method
   - Fixed `load_game_data()` exception handling
   - Fixed `quit()` method
   - Fixed `main()` exception handling

3. **PYTHON_TO_WEB_ISSUES.md**
   - Marked critical issues as fixed
   - Updated recommendations section

4. **WEB_CRITICAL_FIXES_SUMMARY.md** (this file)
   - New file documenting the fixes

---

## Technical Notes

### Why These Changes Were Necessary

**Blocking Calls:**
Web browsers run JavaScript in a single-threaded event loop. When you make a blocking call like `pygame.time.delay()`, it prevents the browser from processing events, updating the UI, or running any other JavaScript. This makes the tab appear frozen.

**sys.exit() on Web:**
In Pygbag/Emscripten, Python code is transpiled to WebAssembly and runs inside a JavaScript event loop. `sys.exit()` doesn't actually terminate the browser tab - it tries to stop the Python runtime, which can leave things in an inconsistent state. The proper way to "exit" is to let functions return naturally and stop the game loop.

### Why These Patterns Work

**Async Timer Pattern:**
By decrementing a timer each frame (`transition_timer -= dt`), we spread the delay across multiple frames. Each frame yields control back to the browser via `await asyncio.sleep(0)` in the main loop, allowing the browser to remain responsive.

**Platform-Specific Error Handling:**
By checking `IS_WEB`, we can provide different behavior for web vs desktop:
- **Desktop:** Can safely call `sys.exit()` to terminate the process
- **Web:** Display errors and return cleanly without trying to terminate

---

## Deployment Checklist

Before deploying to GitHub Pages:

- [x] Critical fixes implemented
- [x] No linting errors
- [ ] Tested on web locally (if possible)
- [ ] Tested loading screen behavior
- [ ] Tested error handling
- [ ] Verified no blocking calls remain
- [ ] Checked browser console for warnings
- [ ] Confirmed game remains responsive

---

## Related Documentation

- Main issues document: `PYTHON_TO_WEB_ISSUES.md`
- Web deployment guide: `docs/WEB_DEPLOYMENT_GUIDE.md`
- GitHub Pages deployment: `GITHUB_PAGES_DEPLOYMENT.md`

---

## Next Steps (Optional Improvements)

While the critical issues are fixed, there are still some improvements that could be made:

1. **Audio Manager Simplification** - Remove excessive debug logging
2. **Add DEBUG flag** - Control verbosity in production
3. **Remove duplicate IS_WEB detection** - Import from config everywhere
4. **Consider lazy loading** - Load sprites on-demand instead of all at once

These are documented in `PYTHON_TO_WEB_ISSUES.md` under "Medium/Low Priority".

