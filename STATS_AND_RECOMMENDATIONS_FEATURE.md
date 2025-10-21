# Gacha Statistics and Recommendations Feature - Complete

## Overview
This update implements a comprehensive statistics tracking system with an info popup on the inventory screen and a recommendation system that guides players to the most beneficial gacha machine.

## Features Implemented

### 1. Pull Tracking System
**Files**: `src/managers/game_data.py`, `src/states/gacha_buy_state.py`, `src/states/gacha_outcome_state.py`

- Added methods to track pulls by version:
  - `record_pull(version, count)` - Records pulls for each gacha machine
  - `get_total_pulls()` - Returns total pulls across all versions  
  - `get_pulls_by_version(version)` - Returns pulls for specific version

- Pull tracking is automatically called when:
  - Single pull is performed (records 1 pull)
  - 10-pull is performed (records 10 pulls)
  - Works from both gacha_buy_state and gacha_outcome_state (pull again button)

- Statistics are persisted in save file under `stats` object:
  ```json
  {
    "total_pulls": 150,
    "pulls_by_version": {
      "Red": 50,
      "Blue": 60,
      "Yellow": 40
    }
  }
  ```

### 2. Expected Pulls Calculator
**File**: `src/utils/gacha_stats.py`

New utility class `GachaStats` with methods:

- **`calculate_expected_pulls_for_version(pokemon_list, rarities_dict, version, owned_pokemon)`**:
  - Calculates expected remaining pulls to complete a specific version's collection
  - Uses coupon collector problem with weighted probabilities
  - Accounts for:
    - Two-step gacha system (rarity → pokemon)
    - Version-specific weights
    - Already owned Pokemon
    - Individual Pokemon weights within rarities

- **`calculate_expected_pulls_from_scratch(pokemon_list, rarities_dict)`**:
  - Calculates expected total pulls to complete entire 151 Pokemon collection from scratch
  - Finds optimal strategy across all three versions
  - Accounts for version exclusives
  - Provides benchmark for player progress

- **`find_recommended_version(pokemon_list, rarities_dict, owned_pokemon)`**:
  - Determines which gacha machine needs the most pulls to complete
  - Returns tuple of (version_name, expected_pulls)
  - Used to display "RECOMMENDED" badge

### 3. Statistics Popup
**File**: `src/ui/stats_popup.py`

New `StatsPopup` component that displays:

- **Total Pulls Done**: Sum of all pulls across versions
- **Pulls by Version**: Breakdown showing Red/Blue/Yellow pulls
- **Expected Remaining Pulls**: For each version, how many more pulls are needed
- **Expected Pulls from Scratch**: Theoretical minimum pulls to complete collection

Features:
- Semi-transparent overlay background
- Styled popup with dark gray background and border
- Yellow section headers
- Close button
- Can be closed with ESC or clicking outside
- Formatted numbers with commas for readability

### 4. Info Button on Inventory
**File**: `src/states/inventory_state.py`

- Added "INFO" button next to "RESET" button in top-right
- Blue color theme (50, 100, 150)
- Clicking opens the stats popup
- Popup is rendered on top of inventory screen
- Event handling prioritizes popup when showing

### 5. Recommended Badge on Gacha Machines
**File**: `src/states/gacha_buy_state.py`

- Yellow "RECOMMENDED" badge displays below the machine button
- Calculated dynamically based on current owned Pokemon
- Shows which machine will be most efficient for completing collection
- Badge styling:
  - Yellow text on dark background
  - Yellow border
  - Positioned below machine button

## Technical Implementation

### Algorithm: Coupon Collector with Weights

The expected pulls calculation uses an approximation of the weighted coupon collector problem:

```
E[T] ≈ Σ(1/p_i) for all unowned Pokemon i

where p_i = P(rarity) × P(pokemon | rarity)
        = (rarity_weight / total_rarity_weight) × (pokemon_weight / rarity_total_weight)
```

This provides a good estimate for how many pulls are needed to collect all remaining Pokemon.

### Data Flow

1. **Pull Occurs** → `record_pull()` updates stats → Saved to JSON
2. **Open Inventory** → Click "INFO" button
3. **Stats Calculated**:
   - Load current owned Pokemon
   - Calculate expected pulls for each version
   - Calculate total expected from scratch
   - Find recommended version
4. **Display Popup** → Shows all statistics
5. **Gacha Screen** → Badge shows on recommended machine

### Integration Points

- **SaveManager**: Stats are saved/loaded with game data
- **GameData**: Tracks pulls and provides query methods
- **GachaStats**: Pure calculation utility (no state)
- **InventoryState**: Hosts info button and popup
- **GachaBuyState**: Displays recommendation badge
- **GachaOutcomeState**: Records pulls from "pull again"

## UI/UX Improvements

1. **Transparency**: Stats popup provides insight without being overwhelming
2. **Guidance**: Recommended badge helps new players make informed decisions
3. **Progress Tracking**: Players can see how many pulls they've done and estimate completion
4. **Benchmarking**: "Expected from scratch" provides context for player efficiency

## Testing

All features have been implemented and integrated. The application should:
- Track pulls correctly
- Display accurate statistics
- Show recommended badge on correct machine
- Open/close popup properly
- Persist pull counts across sessions

## Files Modified

1. `src/managers/game_data.py` - Pull tracking methods
2. `src/states/gacha_buy_state.py` - Record pulls, calculate recommendation, display badge
3. `src/states/gacha_outcome_state.py` - Record pulls from "pull again"
4. `src/states/inventory_state.py` - Info button, stats popup integration
5. `src/ui/stats_popup.py` - NEW: Statistics popup component
6. `src/utils/gacha_stats.py` - NEW: Statistics calculation utility

## Files Created

- `src/utils/gacha_stats.py` - Gacha statistics calculations
- `src/ui/stats_popup.py` - Statistics popup UI component

All changes maintain consistency with existing code architecture and follow the project's design patterns.

