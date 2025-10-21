# Stats and Reset Update

## Summary
Updated the statistics and inventory reset functionality to ensure accurate calculations and proper data clearing.

## Changes Completed

### 1. Pull Statistics Reset on Inventory Reset
**Location**: `src/managers/game_data.py`

Modified the `reset_inventory()` method to also reset pull statistics:

```python
def reset_inventory(self):
    """Reset all owned Pokemon and pull statistics (for reset button)"""
    self.pokemon_owned = {}
    self.newly_acquired = []
    # Reset pull statistics
    self.stats['total_pulls'] = 0
    self.stats['pulls_by_version'] = {'Red': 0, 'Blue': 0, 'Yellow': 0}
    print("Inventory and pull statistics reset")
```

**What This Does:**
- When the player clicks the RESET button in the Pokédex, it now clears:
  - All owned Pokemon
  - Newly acquired list
  - Total pull counter
  - Individual pull counters for Red, Blue, and Yellow versions
- This provides a complete fresh start for the player

### 2. Pulls From Scratch Recalculation
**Status**: Already Working Correctly

**Verification:**
- The `calculate_expected_pulls_from_scratch()` method in `src/utils/gacha_stats.py` is called fresh every time the stats popup is opened
- No caching is performed anywhere in the calculation chain
- The calculation reads directly from:
  - `resource_manager.pokemon_list` (loaded from CSV at game start)
  - `resource_manager.rarities_dict` (loaded from CSV at game start)
- This means any changes to the CSV files will be reflected when the game is relaunched

**How It Works:**
1. Player opens the INFO popup in the Pokédex
2. `_show_stats()` is called in `inventory_state.py`
3. Fresh calculations are performed:
   - `calculate_expected_pulls_for_version()` for each version (Red, Blue, Yellow)
   - `calculate_expected_pulls_from_scratch()` for the complete collection
4. Results are passed to the `StatsPopup` for display
5. No values are cached between popup opens

**What This Means:**
- The "Expected From Scratch" value always reflects the current game state
- Changes to Pokemon weights in the CSV (like the Legendary birds change from 1 to 2 in Yellow) are immediately reflected on next game launch
- The calculation accounts for:
  - Current owned Pokemon
  - Version-specific weights
  - Rarity-based probabilities
  - Version exclusives

## Testing Recommendations

### Test Reset Functionality:
1. Start game with some owned Pokemon and recorded pulls
2. Open INFO popup and note the pull statistics
3. Click RESET button
4. Open INFO popup again
5. Verify:
   - "Total Pulls Done" shows 0
   - "Pulls by Version" all show 0
   - "Expected Remaining Pulls" equals "Expected From Scratch" for each version

### Test Recalculation on Launch:
1. Make a note of current "Expected From Scratch" value
2. Close the game
3. Modify Pokemon weights in `data/pokemon_gen1.csv` (e.g., change a weight)
4. Relaunch the game
5. Open INFO popup
6. Verify "Expected From Scratch" has changed to reflect the new weights

## Technical Notes

### Coupon Collector Problem
The expected pulls calculation uses the coupon collector problem with weighted probabilities:
- For each unowned Pokemon, calculate its probability: `P(pokemon) = P(rarity) × P(pokemon|rarity)`
- Expected pulls: `E[T] ≈ Σ(1/P_i)` for all unowned Pokemon

### Version Exclusives Handling
The "from scratch" calculation:
1. Identifies the version with best coverage (usually Yellow with 151 Pokemon available)
2. Calculates base expected pulls for that version
3. Adds expected pulls for exclusives from other versions
4. Accounts for weighted distribution within each rarity tier

### No Caching Design
The system intentionally avoids caching to ensure:
- Always accurate to current game state
- Reflects CSV changes on reload
- Simple to understand and maintain
- No risk of stale data bugs

## Files Modified
1. `src/managers/game_data.py` - Added pull statistics reset to `reset_inventory()`

## Files Verified (No Changes Needed)
1. `src/utils/gacha_stats.py` - Already calculates fresh every time
2. `src/states/inventory_state.py` - Already calls calculations fresh on popup open
3. `src/ui/stats_popup.py` - Receives fresh data, doesn't cache

