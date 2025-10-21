# Pokémon Blue Gacha System Logic

## Two-Step Weighted Gacha System

### Step 1: Roll for Rarity
Roll a random number based on the rarity weights defined in `rarity_drop_weights.csv`:

| Rarity    | Weight | Probability |
|-----------|--------|-------------|
| Common    | 42     | 42.0%       |
| Uncommon  | 36     | 36.0%       |
| Rare      | 15     | 15.0%       |
| Epic      | 6      | 6.0%        |
| Legendary | 1      | 1.0%        |

**Total Weight: 100**

### Step 2: Roll for Pokémon Within Rarity
Once a rarity is determined, filter all Pokémon from `pokemon_gen1.csv` that match that rarity, then roll based on their individual weights.

#### Weight System
- Each Pokémon has a `Weight` value in the CSV
- Default weight is **1** (equal chance within rarity)
- Setting a Pokémon's weight to **2** makes it **twice as likely** as weight-1 Pokémon in the same rarity
- Setting a weight to **0.5** makes it **half as likely** as weight-1 Pokémon

#### Example
If the rarity roll results in "Uncommon":
1. Filter all Uncommon Pokémon from the CSV (52 total)
2. Sum their weights (if all are 1, total = 52)
3. Roll a weighted random selection

**If Bulbasaur (Uncommon) has weight 2 and all others have weight 1:**
- Total Uncommon weight = 53 (52 + 1 extra from Bulbasaur)
- Bulbasaur probability = 2/53 = 3.77%
- Each other Uncommon = 1/53 = 1.89%

### Implementation Flow
```
1. Generate random number (0-99)
2. Determine rarity based on rarity weights
3. Query pokemon_gen1.csv for all Pokémon with matching rarity
4. Calculate total weight for that rarity tier
5. Perform weighted random selection based on individual weights
6. Return selected Pokémon
```

### Data Files
- **rarity_drop_weights.csv**: Rarity tier weights for Step 1
- **pokemon_gen1.csv**: Complete Pokémon data including individual weights for Step 2

### Benefits
- Easy to adjust overall rarity distribution (modify rarity weights)
- Fine-grained control over individual Pokémon rates (modify individual weights)
- Uniform distribution by default (all weights = 1)
- Can create "featured" Pokémon by increasing their weight temporarily
- Maintains balance within rarity tiers while allowing customization

