# Random Background Music System

## Overview
The game now features a dynamic background music system that randomly selects from 8 tracks and changes music on certain user actions.

## Features Implemented

### 1. Random Music Selection at Startup
- On game load, the system discovers all available background music tracks (background1.mp3 - background8.mp3)
- All 8 tracks are available for rotation
- Plays one of the tracks at random when the game starts

### 2. Music Changes on Unmute
- When the player unmutes the music (via MUTE/UNMUTE button), a new random track is selected
- The system ensures a different track is played (won't repeat the currently playing track if multiple tracks exist)

### 3. Music Changes on Currency Click
- When the player clicks on the Pokédollar currency display, a new random track is selected and played
- This only happens if music is not currently muted
- Provides a fun way for players to change the background music

## Technical Implementation

### AudioManager Updates (`src/managers/audio_manager.py`)
- Added `background_tracks: List[str]` to store available music tracks
- Added `load_background_music_tracks()` method to discover and load all background music files
- Added `play_random_background_music()` method that:
  - Filters out the currently playing track (if multiple exist)
  - Randomly selects a new track
  - Plays it with infinite loop

### Loading State Updates (`src/states/loading_state.py`)
- Now calls `audio_manager.load_background_music_tracks()` during asset loading
- Calls `audio_manager.play_random_background_music()` to start the first random track

### Inventory State Updates (`src/states/inventory_state.py`)
- `_toggle_mute()` method now calls `play_random_background_music()` when unmuting
- Currency click handler now calls `play_random_background_music()` (if not muted)

## Music Track Selection Strategy
The system:
1. Finds all 8 available background tracks
2. Randomly shuffles them for variety
3. All tracks are available for selection
4. When playing, avoids repeating the current track

This ensures maximum variety with 8 unique tracks to cycle through.

## User Experience Benefits
- **Variety**: Players hear different music each time they play (8 unique tracks!)
- **Control**: Players can easily change music by clicking the currency or toggling mute
- **Non-intrusive**: Music changes feel natural and reward player interaction
- **Fresh Sessions**: Each game session shuffles all 8 tracks for a unique listening experience

## Future Enhancements (Optional)
- Add a dedicated "Next Track" button
- Display current track name
- Allow players to favorite specific tracks
- Implement playlist customization

