# Items Gacha Rarity Weights Implementation

## Summary
Added `Items_Weight` column to the rarity system, allowing the Items Gacha to use configurable rarity weights from the CSV instead of hardcoded values.

---

## Changes Made

### 1. **Updated CSV File** ✅
**File**: `data/rarity_drop_weights.csv`

**Before**:
```csv
Rarity,Red_Weight,Blue_Weight,Yellow_Weight,Color
Common,42,42,41,#FFFFFF
Uncommon,36,36,36,#1EFF00
Rare,15,15,15,#0070DD
Epic,6,6,6,#A335EE
Legendary,1,1,2,#FF8000
```

**After**:
```csv
Rarity,Red_Weight,Blue_Weight,Yellow_Weight,Items_Weight,Color
Common,42,42,41,42,#FFFFFF
Uncommon,36,36,36,36,#1EFF00
Rare,15,15,15,15,#0070DD
Epic,6,6,6,6,#A335EE
Legendary,1,1,2,1,#FF8000
```

**Items_Weight Values**:
- Common: 42 (~42%)
- Uncommon: 36 (~36%)
- Rare: 15 (~15%)
- Epic: 6 (~6%)
- Legendary: 1 (~1%)

---

### 2. **Updated Rarity Data Structure** ✅
**File**: `src/data/rarity_data.py`

**Added**:
- `items_weight: int` field to the Rarity dataclass
- Support for "Items" in `get_weight_for_version()` method

**Code**:
```python
@dataclass
class Rarity:
    name: str
    red_weight: int
    blue_weight: int
    yellow_weight: int
    items_weight: int      # NEW
    color_hex: str
    
    def get_weight_for_version(self, version: str) -> int:
        if version == "Red":
            return self.red_weight
        elif version == "Blue":
            return self.blue_weight
        elif version == "Yellow":
            return self.yellow_weight
        elif version == "Items":    # NEW
            return self.items_weight
        else:
            return 0
```

---

### 3. **Updated CSV Loader** ✅
**File**: `src/data/csv_loader.py`

**Changes**:
- Added `'Items_Weight'` to expected headers
- Added `items_weight=int(row['Items_Weight'])` to Rarity constructor

**Code**:
```python
expected_headers = ['Rarity', 'Red_Weight', 'Blue_Weight', 'Yellow_Weight', 'Items_Weight', 'Color']

rarity = Rarity(
    name=row['Rarity'].strip(),
    red_weight=int(row['Red_Weight']),
    blue_weight=int(row['Blue_Weight']),
    yellow_weight=int(row['Yellow_Weight']),
    items_weight=int(row['Items_Weight']),  # NEW
    color_hex=row['Color'].strip()
)
```

---

### 4. **Updated Items Gacha Logic** ✅
**File**: `src/logic/items_gacha.py`

**Changes in `_roll_for_rarity()`**:
```python
# Before (hardcoded fallback):
weight = rarity.weight if hasattr(rarity, 'weight') else 10

# After (use Items_Weight):
weight = rarity.get_weight_for_version("Items")
```

**Changes in `calculate_item_drop_rate()`**:
```python
# Before:
total_rarity_weight = sum(
    rarity.weight if hasattr(rarity, 'weight') else 10
    for rarity in rarities_dict.values()
)
rarity_weight = rarity.weight if hasattr(rarity, 'weight') else 10

# After:
total_rarity_weight = sum(
    rarity.get_weight_for_version("Items")
    for rarity in rarities_dict.values()
)
rarity_weight = rarity.get_weight_for_version("Items")
```

---

## Benefits

### 1. **Consistency** 
- Items Gacha now uses the same rarity weight system as Pokemon Gachas
- All weights centralized in one CSV file

### 2. **Configurability**
- Can easily adjust Items Gacha rarity distribution without code changes
- Edit `Items_Weight` column in CSV to rebalance

### 3. **Flexibility**
- Can make Items Gacha have different distribution than Pokemon
- Example: Could increase Legendary weight to 2 for more exciting pulls

### 4. **Maintainability**
- No more hardcoded fallback values
- Single source of truth for all rarity weights

---

## Current Distribution

Based on `Items_Weight` column:

| Rarity | Weight | Probability | Expected per 100 pulls |
|--------|--------|-------------|------------------------|
| Common | 42 | 42.0% | 42 |
| Uncommon | 36 | 36.0% | 36 |
| Rare | 15 | 15.0% | 15 |
| Epic | 6 | 6.0% | 6 |
| Legendary | 1 | 1.0% | 1 |
| **Total** | **100** | **100%** | **100** |

---

## Example Adjustments

### To Make Items More Exciting:
```csv
Rarity,Red_Weight,Blue_Weight,Yellow_Weight,Items_Weight,Color
Common,42,42,41,30,#FFFFFF
Uncommon,36,36,36,35,#1EFF00
Rare,15,15,15,20,#0070DD
Epic,6,6,6,10,#A335EE
Legendary,1,1,2,5,#FF8000
```
→ 5% Legendary chance (5x more than Pokemon!)

### To Make Items More Conservative:
```csv
Items_Weight
50  (Common)
40  (Uncommon)
8   (Rare)
2   (Epic)
0   (Legendary - no Master Balls!)
```

---

## Testing

✅ **To Test**:
1. Load game → Should load without errors
2. Open Items Gacha
3. Perform 1-pull and 10-pull
4. Verify rarities match expected distribution
5. Check info popup shows correct drop rates

---

## Status

✅ **COMPLETE**

All 4 files updated:
1. ✅ `data/rarity_drop_weights.csv` - Added Items_Weight column
2. ✅ `src/data/rarity_data.py` - Added items_weight field
3. ✅ `src/data/csv_loader.py` - Load Items_Weight from CSV
4. ✅ `src/logic/items_gacha.py` - Use Items_Weight for calculations

The Items Gacha now uses configurable rarity weights from the CSV file!

