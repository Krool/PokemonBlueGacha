# Pokémon Blue Gacha - GUI Specification

## Overview
A single-player offline game where users roll on Pokémon with a gacha system and manage their collection.

## Player Resources
- **Gold**: Players start with 0 gold
- **Add Gold Button**: Adds 10,000 gold to balance
- **Save System**: Player progress (gold + owned Pokémon) saved to JSON file, persists between launches

## Game States
1. Loading
2. Inventory
3. GachaBuy
4. GachaAnimation
5. GachaOutcome

---

## STATE: Loading
The loading and splash screen displayed when game first opens.

**Visual Elements:**
- Display `Assets/logo.png`
- Loading bar that progresses automatically with satisfying animation
- Purely aesthetic (all assets already loaded)

**Audio:**
- Background music starts: `Assets/Sounds/background` (looped)

---

## STATE: Inventory
Main collection management screen displaying all 151 Gen 1 Pokémon.

### Pokemon Tile Display
Each Pokémon tile shows:
- **Center**: Pokémon sprite image
- **Top Left**: Type icons (stacked vertically, both types shown with equal prominence)
- **Bottom Right**: Amount owned (e.g., "x3")
- **Background**: 
  - If owned: Colored by Type1 color from pokemon_types.csv
  - If unowned: Gray
- **Outline**: Colored by rarity (with glow/shimmer effect)
  - Rarity colors from rarity_drop_weights.csv
- **NEW Indicator**: Display "NEW!" badge for first-time catches

### Sort Options
Three sort buttons above the list (icons: #, star, x):
1. **Pokédex Number** (default sort)
2. **Rarity** (descending)
3. **Amount Owned** (descending)

**Behavior**: Tapping the same sort button reverses the order

### Filter Options
- **"Owned" Checkbox**: 
  - Unchecked: Show all 151 Pokémon
  - Checked: Show only owned Pokémon
  - When no Pokémon owned: Display "No pokemon owned" text

### Action Buttons (below list)
1. Open Gacha page
2. Reset owned count (no confirmation)
3. Close game (no confirmation)

---

## STATE: GachaBuy
Gacha purchase screen with three machine options.

**Visual Elements:**
- Display `Assets/gacha.png`
- Gold balance display
- **Three Gacha Machine Options:**
  - **Red Machine**: Original Red version pool
    - Single Pull: 1,000 gold | 10-Pull: 9,000 gold
    - Contains Red exclusives (Growlithe, Arcanine, Scyther, etc.)
  - **Blue Machine**: Original Blue version pool
    - Single Pull: 1,000 gold | 10-Pull: 9,000 gold
    - Contains Blue exclusives (Sandshrew, Vulpix, Pinsir, etc.)
  - **Yellow Machine**: Special Pikachu edition
    - Single Pull: 1,500 gold | 10-Pull: 13,500 gold (50% higher cost)
    - **DOUBLE legendary drop rate** (2x vs 1x)
    - Missing some early evolutions and Pokémon
- **Machine Selection UI:**
  - Buttons/tabs to select which machine
  - Selected machine displays name and description
  - Shows costs for Single Pull and 10-Pull for selected machine
- Return to Inventory button

**Behavior:**
- Player selects one of three machines
- If player has enough gold: Begin GachaAnimation
- If not enough gold: Show popup
  - Message: "Not enough gold"
  - Button: "Add Gold" (adds 10,000 gold, closes popup)

**Gacha Roll Logic (Two-Step Weighted System per Machine):**
1. Roll random value between 0 and sum of rarity weights for selected machine version
2. Determine rarity tier
3. Roll random value between 0 and sum of qualifying Pokémon weights at that rarity for selected machine version
4. Determine specific Pokémon outcome (only from Pokémon with non-zero weight for that version)
5. Add Pokémon to player inventory

---

## STATE: GachaAnimation
Animated gacha machine shake based on outcome rarity.

**Animation Specifications:**
- **Duration**: Max 2 seconds (scales with rarity)
- **Intensity**: Increases with rarity
- **Pattern**: 
  - Lower rarities: Horizontal/vertical shake
  - Higher rarities: Add rotations
- **Visual**: Colorize `Assets/gacha.png` based on rarity outcome color
- **Skip**: Player can click anywhere to skip animation

**Audio:**
- Common/Uncommon/Rare/Epic: Randomly choose from `roll1`, `roll2`, or `roll3`
- Legendary: Play `legendary` sound effect

**Transition**: After animation completes or is skipped, show GachaOutcome

---

## STATE: GachaOutcome
Display rolled Pokémon results.

**Visual Elements:**
- Display 1 or 10 Pokémon tiles (based on pull type)
- **10-Pull**: Show all 10 in a grid simultaneously
- **Duplicate Pulls**: Show separate tiles (e.g., 3 Pidgey = 3 separate tiles)
- Tiles use same style as Inventory (with type background, rarity outline, "NEW!" badges)

**Action Buttons:**
1. **Roll Again**: Same cost/amount as previous roll
   - If not enough gold: Same popup flow as GachaBuy
2. **Return to Inventory**

---

## Audio System
- **Background Music**: `Assets/Sounds/background` (looped continuously)
- **Roll Sound Effects**:
  - Common/Uncommon/Rare/Epic: Random selection from `roll1`, `roll2`, `roll3`
  - Legendary: `legendary`

---

## Data Files
- `pokemon_gen1.csv`: All 151 Pokémon with sprites, types, rarity, version-specific weights (Red_Weight, Blue_Weight, Yellow_Weight)
- `pokemon_types.csv`: 15 types with icons and hex colors
- `rarity_drop_weights.csv`: 5 rarity tiers with version-specific weights (Red_Weight, Blue_Weight, Yellow_Weight) and hex colors
- `gacha_machines.csv`: 3 gacha machine definitions (Red, Blue, Yellow) with costs and descriptions
- Player save file: JSON format (gold balance + Pokémon inventory counts)

---

## Visual Polish
- Rarity outlines: Glow/shimmer effects
- Sort buttons: Toggle with visual feedback
- Loading bar: Smooth, satisfying animation
- Type backgrounds: Use Type1 color from CSV
- Particle effects: (Future addition)

