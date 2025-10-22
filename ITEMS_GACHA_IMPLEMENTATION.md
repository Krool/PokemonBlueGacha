# Items Gacha Implementation Plan

## Overview
Adding a fourth gacha machine that dispenses Gen 1 items instead of Pokémon.

## ✅ Completed Steps

### 1. Data Creation
- ✅ Created `create_items_data.py` script
- ✅ Generated `data/items_gen1.csv` with 79 items
- ✅ Assigned rarities based on value:
  - Legendary: 2 items (Master Ball, Rare Candy)
  - Epic: 8 items (high-value TMs, vitamins)
  - Rare: 13 items (evolution stones, important TMs)
  - Uncommon: 27 items (mid-value items)
  - Common: 29 items (basic items)
- ✅ Set weight of 10 for all items (uniform within rarity)

### 2. Icons
- ✅ Downloaded 50 item icons from PokéSprite repository
- ✅ Created 29 placeholder icons for missing items
- ✅ All icons saved to `Assets/Sprites/Items/`

### 3. Data Structures
- ✅ Created `src/data/item_data.py` with Item class
- ✅ Updated `src/data/csv_loader.py` with `load_items()` method

### 4. Configuration
- ✅ Updated `data/gacha_machines.csv` with Items Machine:
  - Cost: 800 / 7,200 (20% cheaper than Red/Blue)
  - Description: "Roll for valuable items! Evolution stones, vitamins, TMs, and more!"
- ✅ Updated `src/config.py`:
  - Added `ITEMS_CSV` path
  - Added `GACHA_ITEM_PATH` for machine image

## 🚧 Remaining Tasks

### 5. Load Items Data
**File**: `src/main.py`
- Load items using `CSVLoader.load_items(ITEMS_CSV)`
- Add `items_list` to resource manager
- Handle loading errors

### 6. Resource Manager Updates
**File**: `src/managers/resource_manager.py`
- Add `self.items_list: List[Item] = []`
- Create `get_item_by_number()` method
- Create `get_item_icon()` method for loading item sprites
- Preload item icons similar to Pokémon sprites

### 7. Game Data Updates
**File**: `src/managers/game_data.py`
- Add `self.items_owned: Dict[str, int] = {}`  # item_number -> count
- Add `add_item(item_number)` method
- Add `get_item_count(item_number)` method
- Add `has_item(item_number)` method
- Add `get_total_items_count()` method
- Update `save()` to include items
- Update `reset_inventory()` to clear items

### 8. Save Manager Updates
**File**: `src/managers/save_manager.py`
- Update `save_game()` to accept `items_owned` parameter
- Update save data dictionary to include `"items_owned": items_owned`
- Update `get_default_save()` to include `"items_owned": {}`

### 9. Items Gacha Logic
**File**: `src/utils/gacha_logic.py` (or new file)
- Create `perform_item_gacha_pull()` function
- Use same two-step weighted system:
  1. Roll for rarity using rarity weights
  2. Roll for item within that rarity using item weights
- Return list of item numbers

### 10. Gacha Buy State Updates
**File**: `src/states/gacha_buy_state.py`
- Add "Items" to machine selection
- Load `gacha_item.png` image (or use placeholder)
- Display list of sample items instead of Pokémon
- Handle Items machine selection differently:
  - Show item icons instead of Pokémon
  - Show item categories/types
  - Calculate % chance for new items
- Update pull logic to call items gacha for Items machine

### 11. Gacha Animation State Updates
**File**: `src/states/gacha_animation_state.py`
- Accept `is_items` parameter
- Display item icons instead of Pokémon sprites
- Use same animation effects
- Play appropriate sounds

### 12. Gacha Outcome State Updates
**File**: `src/states/gacha_outcome_state.py`
- Accept `is_items` parameter
- Display item tiles instead of Pokémon tiles
- Show item names, icons, rarities
- Track NEW items
- Update inventory counts

### 13. Items Info Popup
**File**: `src/ui/items_info_popup.py` (new file)
- Similar to `gacha_info_popup.py`
- Show all 79 items with drop rates
- Scrollable list
- Show item name, category, rarity, % chance

### 14. Expected Value Calculation
**File**: `src/utils/gacha_stats.py`
- Add `calculate_items_expected_value()` method
- Formula: Sum of (item_value × drop_probability) for all items
- Display in items info popup
- Show expected value per pull and per 10-pull

### 15. Stats Popup Updates
**File**: `src/ui/stats_popup.py`
- Add items statistics:
  - Total items owned (X/79)
  - Items pulls count
  - Expected value per pull
- Display on separate tab or section

### 16. Inventory State Updates (Optional)
**File**: `src/states/inventory_state.py`
- Add "Items" tab/button
- Display owned items in grid
- Show item counts
- Filter/sort options

### 17. Create/Add gacha_item.png
**File**: `Assets/Sprites/Main/gacha_item.png`
- Need an image for the Items gacha machine
- Could be:
  - Item chest/box
  - Bag of items
  - Poké Mart counter
  - Generic slot machine with items
- Size: Similar to other gacha images (~400-600px)

## 📊 Items Distribution

| Rarity | Count | Examples |
|--------|-------|----------|
| Legendary | 2 | Master Ball, Rare Candy |
| Epic | 8 | Earthquake TM, Hyper Beam TM, HP Up |
| Rare | 13 | Evolution Stones, Ice Beam TM |
| Uncommon | 27 | Full Restore, Max Potion, Revive |
| Common | 29 | Potions, Antidotes, basic TMs |

## 🎯 Key Design Decisions

### Pricing
- **20% cheaper** than Pokémon gachas
- Single: 800 vs 1,000
- 10-Pull: 7,200 vs 9,000
- Rationale: Items are consumable/one-time use

### Weight System
- All items have weight = 10
- Uniform distribution within each rarity
- Same two-step system as Pokémon

### Expected Value
- Calculate monetary value of average pull
- Help players decide if it's worth it
- Compare to buying items directly (if possible)

### Items Excluded
✅ Already excluded from CSV:
- Badges (8 items)
- Bicycle
- ????? glitch items
- Fossils (Dome, Helix, Old Amber)
- Keys (Card Key, Secret Key, Lift Key)
- Oak's Parcel
- Silph Scope
- Poké Flute
- HMs (5 items)
- Town Map

## 🔄 Integration Points

### Resource Manager
```python
self.items_list = []  # List[Item]
self.gacha_item_image = None  # pygame.Surface
```

### Game Data
```python
self.items_owned = {}  # {item_number: count}
```

### Gacha Logic
```python
def perform_item_gacha_pull(items_list, rarities_dict):
    # Same two-step logic as Pokémon
    # Returns list of item numbers
```

### UI Components
- Item tile component (similar to Pokémon tile)
- Items info popup
- Items grid display

## 📈 Testing Checklist

- [ ] Items load correctly from CSV
- [ ] Item icons display properly
- [ ] Items Machine appears in gacha selection
- [ ] Single pull dispenses 1 item
- [ ] 10-pull dispenses 10 items
- [ ] Item counts update in inventory
- [ ] NEW tag appears for first-time items
- [ ] Rarity distribution matches expected rates
- [ ] Expected value calculation is accurate
- [ ] Items stats display correctly
- [ ] Save/load includes items data
- [ ] Reset clears items inventory

## 📝 Documentation Updates Needed

After implementation:
- Update README.md with Items Machine info
- Update FEATURES.md with items gacha details
- Add to DEVELOPMENT_HISTORY.md
- Create ITEMS_GACHA_COMPLETE.md with summary

## 🎨 Visual Assets Needed

1. **gacha_item.png** - Items gacha machine image
2. Item icons - ✅ Already created (79 icons)
3. Optional: Item bag/inventory icon

## 🔊 Audio (Optional)

- Could use different roll sound for items
- Or keep same sounds as Pokémon gacha

---

**Status**: Foundation complete (data, icons, config)
**Next**: Implement data loading and resource management
**Estimated Remaining**: 10-15 tasks
**Complexity**: Medium-High (requires updates to 8+ files)

