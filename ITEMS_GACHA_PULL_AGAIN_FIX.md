# Items Gacha "PULL AGAIN" Fix

## Issue
When clicking "PULL AGAIN" on the Items gacha outcome screen, the game crashed with:
```
IndexError: list index out of range
```

## Root Cause
The `_roll_same()` method in `gacha_outcome_state.py` was always using the **Pokemon gacha system** (`self.gacha_system.roll_ten()` / `roll_single()`), even when the last pull was from the **Items machine**.

The Pokemon gacha system tried to look up version-specific weights for "Items" (which doesn't exist in the Pokemon weight system), causing an empty weights list and crashing.

## The Fix

**File**: `src/states/gacha_outcome_state.py`

### Changes Made:

1. **Added import**:
   ```python
   from logic.items_gacha import perform_items_gacha
   ```

2. **Updated `_roll_same()` method** to check `self.is_items_gacha`:

```python
# Check if this is Items gacha
if self.is_items_gacha:
    # Perform items gacha
    item_numbers = perform_items_gacha(
        self.resource_manager.items_list,
        self.resource_manager.rarities_dict,
        count=pull_count
    )
    
    # Get item objects
    results = [self.resource_manager.get_item_by_number(num) for num in item_numbers]
    results = [r for r in results if r is not None]
    
    print(f"{pull_count}-pull from Items machine! Gold: {self.game_data.gold}")
    for item in results:
        print(f"  - {item.name} ({item.rarity})")
        self.game_data.add_item(item.number)
    
    self.game_data.save()
    
    # Go to animation
    self.state_manager.change_state('gacha_animation', 
                                    results=results, 
                                    is_ten_pull=self.is_ten_pull, 
                                    machine=self.last_machine, 
                                    owned_before=0, 
                                    is_items_gacha=True)
else:
    # Perform Pokemon gacha (existing logic)
    # ... Pokemon gacha code ...
```

## What Now Works

✅ **PULL AGAIN on Items Gacha**:
- Single-pull → Pulls 1 more item
- 10-pull → Pulls 10 more items
- Uses correct items gacha logic
- Adds items to inventory
- Shows animation
- Displays results with NEW! badges
- Deducts correct cost

✅ **PULL AGAIN on Pokemon Gacha**:
- Still works as before
- Uses Pokemon gacha logic
- Tracks owned_before count correctly

## Testing

- [x] Items 1-pull → PULL AGAIN → Works
- [x] Items 10-pull → PULL AGAIN → Works
- [x] Pokemon 1-pull → PULL AGAIN → Still works
- [x] Pokemon 10-pull → PULL AGAIN → Still works
- [x] Items save to inventory
- [x] NEW! badges appear correctly
- [x] Cost deducted correctly

## Status

✅ **FIXED** - Items gacha PULL AGAIN now works correctly!

