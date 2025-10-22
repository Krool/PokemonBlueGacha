# Audio System Review

## Overview
The audio system has been updated to use a 64-channel architecture that allows simultaneous playback of background music and sound effects on both desktop and web.

## Architecture

### Core Components

#### 1. AudioManager (`src/managers/audio_manager.py`)
- **Initialization:** 64 channels on web, 8 on desktop
- **Background Music:** Uses `pygame.mixer.music` (single dedicated channel)
- **Sound Effects:** Uses `pygame.mixer.Sound` with `pygame.mixer.Channel()` for playback
- **Volume Levels:**
  - Music: 4.7% (0.046875)
  - SFX: 12.5% (0.125)

### Key Methods

#### Sound Effects
- `load_sound(path, name)`: Loads sound as pygame.mixer.Sound object (both desktop and web)
- `play_sound(name, priority=False)`: Plays sound using channel system
  - Finds available channel with `pygame.mixer.find_channel()`
  - Falls back to channel 0 if all 64 channels busy
  - `priority` parameter is maintained for backwards compatibility but unused
- `play_random_click_sound()`: Randomly plays click1, click2, or click3

#### Background Music
- `load_background_music_tracks(path)`: Loads background1.mp3 through background8.mp3
- `play_music(path, loops=-1)`: Plays music on pygame.mixer.music channel
  - Infinite loop by default
  - Handles web autoplay policy (stores pending music if user hasn't interacted)
- `play_random_background_music()`: Randomly selects from loaded tracks
- `stop_music()`: Stops current music

#### Web Compatibility
- `enable_audio_after_interaction(allow_music_start)`: Must be called after first user interaction on web
- `user_interacted`: Flag to track if user has clicked (required for web autoplay)
- `pending_music`: Stores music to play after user interaction

### Usage Throughout Codebase

#### States
1. **inventory_state.py**
   - ✅ Starts/stops music based on mute state in `enter()`
   - ✅ Calls `play_random_background_music()` when entering
   - ✅ Handles mute toggle properly

2. **gacha_animation_state.py**
   - ✅ Uses `play_sound("chaching", priority=True)` for Legendary pulls
   - ✅ Uses `play_sound("roll1/2/3", priority=True)` for normal pulls
   - ✅ Priority flag maintained for backwards compatibility

3. **gacha_outcome_state.py**
   - ✅ Uses `play_sound("gotemall", priority=True)` for collection complete
   - ✅ Uses special `play_click_sound=False` on "PULL AGAIN" button

4. **gacha_buy_state.py**
   - ✅ Passes `audio_manager` to all UI elements
   - ✅ Uses `play_click_sound=False` on 1-PULL and 10-PULL buttons
   - ✅ Handles `enable_audio_after_interaction()` on first user click

5. **loading_state.py**
   - ✅ Loads all sound effects via `load_game_sounds()`
   - ✅ Loads background tracks via `load_background_music_tracks()`
   - ✅ Starts random music after loading
   - ✅ Handles `enable_audio_after_interaction()`

#### UI Components
1. **button.py**
   - ✅ Uses `play_random_click_sound()` if `play_click_sound=True`
   - ✅ Respects `play_click_sound` parameter (defaults to True)
   - ✅ Gacha pull buttons have this disabled to prevent overlap with roll sounds

2. **checkbox.py**
   - ✅ Uses `play_random_click_sound()` on toggle

3. **sort_button.py**
   - ✅ Uses `play_random_click_sound()` on click

### Loaded Sound Effects
- `roll1.mp3`, `roll2.mp3`, `roll3.mp3` - Gacha pull sounds
- `legendary.mp3` - Not currently used (removed to prevent double-sound)
- `chaching.mp3` - Success/Legendary pull sound
- `gotemall.mp3` - Collection complete sound
- `click1.mp3`, `click2.mp3`, `click3.mp3` - UI click sounds
- `background1.mp3` through `background8.mp3` - Background music tracks

## Consistency Issues Found

### Minor Cleanup Needed
1. **Unused Variables:**
   - `self.sfx_channels = []` - Never used (line 23)
   - `self.sound_paths = {}` - Populated but never used (line 21)
   
2. **Documentation:**
   - Some comments reference old single-channel system
   - `priority` parameter documentation should clarify it's unused

## Recommendations

### 1. Clean Up Unused Code
Remove `self.sfx_channels` and `self.sound_paths` if not needed for future features.

### 2. Simplify Priority Parameter
Since the channel system handles everything automatically, consider removing the `priority` parameter entirely or document it clearly as "maintained for backwards compatibility, currently unused".

### 3. Test on Web
Since we're now using `pygame.mixer.Sound()` on web (which was previously commented as "doesn't work"), we should thoroughly test:
- ✅ Sound effects play simultaneously
- ✅ Background music continues while SFX play
- ✅ No browser console errors
- ✅ No popup errors

## Current State
✅ **Consistent Implementation**: All audio calls use proper methods
✅ **Channel Architecture**: 64 channels allow simultaneous playback
✅ **Web Compatibility**: Proper autoplay policy handling
✅ **Volume Management**: Consistent volume levels across all sounds
✅ **Click Sound Control**: Gacha buttons properly disable clicks to prevent overlap

## Summary
The audio system is **well-structured and consistent** across the codebase. The only issues are minor cleanup opportunities (unused variables) and the need to test the new channel-based system on web to ensure `pygame.mixer.Sound()` works as expected with Pygbag.

