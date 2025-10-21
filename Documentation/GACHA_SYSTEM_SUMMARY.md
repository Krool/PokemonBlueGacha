# Pokémon Blue Gacha System - Complete Summary

## System Architecture

### Two-Step Weighted Gacha System

#### Step 1: Rarity Roll
Roll a weighted random number based on rarity weights from `rarity_drop_weights.csv`:

| Rarity    | Weight | Probability |
|-----------|--------|-------------|
| Common    | 42     | 42%         |
| Uncommon  | 36     | 36%         |
| Rare      | 15     | 15%         |
| Epic      | 6      | 6%          |
| Legendary | 1      | 1%          |

#### Step 2: Pokémon Roll
Once a rarity is determined, perform a weighted random selection from all Pokémon in that rarity tier using their individual weights from `pokemon_gen1.csv`.

**Formula**: `Probability = (Rarity_Weight / Total_Rarity_Weight) × (Pokemon_Weight / Rarity_Total_Weight)`

## Weight System

### Default Configuration
- All Pokémon currently have `Weight = 1`
- This creates equal probability for all Pokémon within the same rarity tier

### Weight Multiplier Examples

**Example 1: Double Rate**
- Set a Pokémon's weight to `2`
- It becomes **2x more likely** than weight-1 Pokémon in the same rarity
- Bulbasaur (Uncommon, Weight=2): 1.38% chance (instead of 0.69%)

**Example 2: Featured Pokémon**
- Set a Pokémon's weight to `5` 
- It becomes **~4.5x more likely** than others in its rarity
- Great for limited-time featured events

**Example 3: Reduced Rate**
- Set a Pokémon's weight to `0.5`
- It becomes **half as likely** as weight-1 Pokémon
- Useful for making certain Pokémon extra rare within their tier

## Current Drop Rates (All Weights = 1)

### By Rarity Tier
| Rarity    | Count | Rarity % | Per Pokémon % | Expected Pulls |
|-----------|-------|----------|---------------|----------------|
| Common    | 47    | 42.00%   | 0.8936%       | 112            |
| Uncommon  | 52    | 36.00%   | 0.6923%       | 144            |
| Rare      | 35    | 15.00%   | 0.4286%       | 233            |
| Epic      | 12    | 6.00%    | 0.5000%       | 200            |
| Legendary | 5     | 1.00%    | 0.2000%       | 500            |

### Collection Statistics
- **Expected pulls for complete collection**: ~25,837
- **Expected pulls for any legendary**: ~100
- **Expected pulls for specific legendary**: ~500

## Data Files

### 1. `pokemon_gen1.csv`
Complete Pokémon database with columns:
- `Number`: Pokédex number (001-151)
- `Name`: Pokémon name
- `Type1`: Primary type
- `Type2`: Secondary type (empty if single-type)
- `Rarity`: Common, Uncommon, Rare, Epic, or Legendary
- `Weight`: Individual drop weight within rarity (default: 1)

### 2. `rarity_drop_weights.csv`
Rarity tier weights:
- `Rarity`: Tier name
- `Drop_Weight`: Weight for Step 1 roll

### 3. `gacha_calculations.py`
Python calculator that:
- Reads from CSV files
- Calculates probabilities for any weight configuration
- Provides expected pulls and cost analysis
- Supports weighted and uniform distributions

### 4. `gacha_system_logic.md`
Detailed technical documentation of the system logic

## Use Cases

### Standard Play
All weights stay at 1 for balanced gameplay

### Featured Banners
Temporarily increase weight for specific Pokémon:
- Featured starter: Weight = 3
- All others in rarity: Weight = 1

### Seasonal Events
Adjust weights for themed Pokémon:
- Ice types in winter: Weight = 2
- Fire types in winter: Weight = 0.5

### Rate-Up Events
Double rates for specific rarity:
- Increase all Rare Pokémon weights to 2
- Or adjust rarity weight in `rarity_drop_weights.csv`

## Implementation Benefits

✅ **Flexible**: Change individual Pokémon rates without affecting others  
✅ **Balanced**: Rarity tiers maintain overall distribution  
✅ **Transparent**: Easy to calculate and verify probabilities  
✅ **Event-Ready**: Simple to create featured banners  
✅ **Data-Driven**: All rates controlled by CSV files  
✅ **Scalable**: Add more Pokémon or rarities easily

## Testing Tools

Run `python gacha_calculations.py` to see current system analysis  
Run `python gacha_weight_example.py` to see weight system examples

