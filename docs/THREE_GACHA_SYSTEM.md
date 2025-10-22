# Three Gacha System Implementation

## Overview
Updated the Pokémon Blue Gacha game to support three distinct gacha machines based on the original Game Boy versions: Red, Blue, and Yellow.

## Key Changes

### 1. Data Files Updated

#### `data/pokemon_gen1.csv`
- **Changed**: Single `Weight` column → Three columns: `Red_Weight`, `Blue_Weight`, `Yellow_Weight`
- **Version Exclusives**: Set weight to `0` for Pokémon not available in specific versions
  - **Red version excludes**: Sandshrew, Sandslash, Bellsprout, Weepinbell, Victreebel, Meowth, Persian, Vulpix, Ninetales, Pinsir, Magmar, Mew
  - **Blue version excludes**: Ekans, Arbok, Oddish, Gloom, Vileplume, Mankey, Primeape, Growlithe, Arcanine, Scyther, Electabuzz, Mew
  - **Yellow version excludes**: Weedle, Kakuna, Beedrill, Ekans, Arbok, Meowth, Persian, Koffing, Weezing, Raichu, Jynx, Electabuzz, Magmar, Mew

#### `data/rarity_drop_weights.csv`
- **Changed**: Single `Drop_Weight` column → Three columns: `Red_Weight`, `Blue_Weight`, `Yellow_Weight`
- **Yellow Machine Special**: Legendary weight = 2 (double chance), Common weight = 41 (reduced by 1)

#### `data/gacha_machines.csv` (NEW FILE)
Defines the three gacha machine options:

| Version | Single Pull Cost | 10-Pull Cost | Special Features |
|---------|-----------------|--------------|------------------|
| Red     | 1,000           | 9,000        | Original Red exclusives |
| Blue    | 1,000           | 9,000        | Original Blue exclusives |
| Yellow  | 1,500           | 13,500       | **50% higher cost, 2x legendary rate** |

### 2. Code Structure Updates

#### New Data Class: `GachaMachine`
```python
class GachaMachine:
    name: str          # "Red Machine"
    version: str       # "Red", "Blue", or "Yellow"
    cost_single: int   # 1000 or 1500
    cost_10pull: int   # 9000 or 13500
    description: str   # Machine description
```

#### Updated Data Classes

**`Pokemon`**:
- Added: `red_weight`, `blue_weight`, `yellow_weight`
- Added method: `get_weight_for_version(version: str) -> int`

**`Rarity`**:
- Changed: `drop_weight` → `red_weight`, `blue_weight`, `yellow_weight`
- Added method: `get_weight_for_version(version: str) -> int`

#### Updated Loaders
- `CSVLoader.load_pokemon()`: Now reads `Red_Weight`, `Blue_Weight`, `Yellow_Weight` columns
- `CSVLoader.load_rarities()`: Now reads version-specific weight columns
- `CSVLoader.load_gacha_machines()`: New method to load gacha machine definitions

#### Updated Managers
- `ResourceManager`: Added `gacha_machines_dict` storage and `get_gacha_machine()` method
- Config: Added `GACHA_MACHINES_CSV` path constant

### 3. Game Design Updates

#### GachaBuy State (Future Implementation)
- Player selects one of three gacha machines
- UI shows selected machine's name, description, and costs
- Costs vary by machine (Yellow is 50% more expensive)
- Each machine pulls from its version-specific pool

#### Gacha Logic (Two-Step Weighted System Per Version)
1. **Step 1**: Roll on rarity weights for selected version
   - Example: Yellow has 2x chance for Legendary rarity
2. **Step 2**: Roll on qualifying Pokémon for that rarity and version
   - Only Pokémon with non-zero weight for that version are included
   - Individual weights still apply (all currently set to 1 for uniform distribution within rarity)

## Benefits

### Gameplay
- **Strategic Choice**: Players choose between lower cost (Red/Blue) or better legendary rates (Yellow)
- **Collection Variety**: Different machines offer different exclusive Pokémon
- **Authentic Experience**: Mirrors the original Game Boy version differences

### Balance
- **Yellow Premium**: Higher cost balanced by 2x legendary rate (2 vs 1)
- **Version Exclusives**: Creates scarcity and trading potential (future feature)
- **Flexible Weighting**: Can adjust individual Pokémon weights per version if needed

## Reference
Based on: [IGN Pokemon Red/Blue/Yellow Version Exclusives Guide](https://www.ign.com/wikis/pokemon-red-blue-yellow-version/Version_Exclusives)

## Documentation Updates
- ✅ `README.md`: Updated GachaBuy state section with three-machine system
- ✅ `README.md`: Updated Data Files section with new CSV structure
- ✅ All data classes updated with version-specific properties
- ✅ All CSV loaders updated to handle new structure

## Testing Status
- ✅ CSV files updated successfully
- ✅ Data classes updated
- ✅ Loaders updated and integrated
- ⏳ Game running - pending verification
- ⏳ UI implementation - pending (Phase 3)

## Next Steps
1. Verify game loads correctly with new data structure
2. Implement three-machine selection UI in GachaBuy state
3. Update gacha logic to use version-specific weights
4. Test drop rates for each machine
5. Update inventory to show which version each Pokémon came from (optional)

