# Features Guide

Complete guide to all features in Pokémon Blue Gacha.

## 🎰 Gacha System

### Three Gacha Machines

#### Red Machine
- **Cost**: 1,000 / 9,000 Pokédollars (1-pull / 10-pull)
- **Pool**: 146 Pokémon (Red version exclusives)
- **Exclusives**: Growlithe, Arcanine, Oddish, Gloom, Vileplume, Mankey, Primeape, Scyther, Electabuzz
- **Best For**: Collecting Red exclusives

#### Blue Machine
- **Cost**: 1,000 / 9,000 Pokédollars (1-pull / 10-pull)
- **Pool**: 146 Pokémon (Blue version exclusives)
- **Exclusives**: Sandshrew, Sandslash, Vulpix, Ninetales, Meowth, Persian, Bellsprout, Weepinbell, Victreebel, Magmar, Pinsir
- **Best For**: Collecting Blue exclusives

#### Yellow Machine
- **Cost**: 1,500 / 13,500 Pokédollars (1-pull / 10-pull) - 50% premium
- **Pool**: 151 Pokémon (all available)
- **Special**: **2x Legendary drop rate** (2% vs 1%)
- **Best For**: Hunting legendaries (Articuno, Zapdos, Moltres, Mewtwo, Mew)

### Two-Step Gacha Logic

1. **Rarity Roll**: Weighted random selection of rarity tier
2. **Pokémon Roll**: Weighted random selection within that rarity

This ensures rarity distribution matches the configured rates while allowing individual Pokémon weight adjustments.

### Rarity Distribution

| Rarity | Color | Red/Blue Rate | Yellow Rate |
|--------|-------|---------------|-------------|
| Common | White | 42% | 41% |
| Uncommon | Green | 36% | 36% |
| Rare | Blue | 15% | 15% |
| Epic | Purple | 6% | 6% |
| Legendary | Orange | 1% | **2%** |

### Pull Options

- **1-Pull**: Single Pokémon, full price
- **10-Pull**: 10 Pokémon, 10% discount (9,000 vs 10,000)

---

## 📖 Pokédex System

### Display Features

- **Grid Layout**: All 151 Pokémon in Pokédex order
- **Scrollable**: Mouse wheel support
- **Owned Status**: 
  - Owned: Colored by primary type
  - Unowned: Grayed out
- **Count Display**: "x3" shows duplicate count
- **NEW! Badge**: Highlights first-time catches (large, prominent)
- **Rarity Outline**: Color-coded glow effect

### Sort Options

Three sort modes with ascending/descending toggle:

1. **NUM**: Pokédex number (001-151)
2. **RAR**: Rarity (Legendary → Common)
3. **AMT**: Amount owned (most → least)

**Behavior**: Click same button to toggle direction

### Filter Options

- **Owned Checkbox**: Show only owned Pokémon
- When unchecked: Show all 151
- When checked: Show only caught Pokémon

### Progress Display

- **Format**: "X/151 Pokémon"
- **Color**: 
  - White: Incomplete
  - Gold: Complete (151/151)

---

## 📊 Statistics & Analysis

### Stats Panel (INFO button on Pokédex)

Displays comprehensive gacha statistics:

#### Pull History
- Total pulls across all machines
- Pulls per machine (Red/Blue/Yellow)

#### Expected Pulls
- **Per Machine**: Expected pulls to get rarest remaining Pokémon
- **From Scratch**: Total expected pulls to complete collection (sum of all three)

#### Optimal Strategy
- **Cost Display**: Expected Pokédollars to complete collection using optimal strategy
  - Yellow for legendaries (best rate)
  - Red/Blue for exclusives
- **Clickable**: Click the cost to set your money to that amount

### Recommended Machine

- **Badge**: Yellow "RECOMMENDED" label on top of suggested machine
- **Logic**: Recommends machine with most expected pulls remaining
- **Hidden**: When collection is complete

### Featured Pokémon

Each machine displays 3 featured Pokémon:
- **Red**: Red exclusives (Growlithe, Arcanine, Scyther, etc.)
- **Blue**: Blue exclusives (Vulpix, Meowth, Pinsir, etc.)
- **Yellow**: Legendary Pokémon (Articuno, Zapdos, Moltres, Mewtwo, Mew)

Selection is weighted toward rarer Pokémon.

### New Pokémon Chance

Displays percentage chance of pulling a new (not yet owned) Pokémon for selected machine.

---

## 🔍 Drop Rate Transparency

### INFO Button (Gacha Buy Page)

Click INFO to view complete drop rate information:

- **All Pokémon**: Every Pokémon available in selected machine
- **Exact Rates**: Percentage to 4 decimal places (e.g., 0.5432%)
- **Rarity Dots**: Color-coded indicators
- **Scrollable List**: Mouse wheel support
- **Sorted**: By drop rate (rarest first)

### Rate Calculation

Formula: `(Rarity Weight / Total Rarity Weight) × (Pokémon Weight / Total Pokémon Weight in Rarity) × 100`

Example for Mew in Yellow:
- Legendary rarity: 2/100 = 2%
- Mew within Legendary: 1/5 = 20%
- Final rate: 2% × 20% = 0.4%

---

## 🎵 Audio System

### Background Music

- **8 Tracks**: background1.mp3 through background8.mp3
- **Random Selection**: Shuffled on game start
- **No Repeats**: Won't replay current track when changing
- **Change Music**:
  - Click Pokédollar display
  - Toggle mute/unmute
- **Persistent Mute**: Setting saved between sessions

### Sound Effects

| Sound | Trigger |
|-------|---------|
| roll1-3.mp3 | Random for Common/Uncommon/Rare/Epic pulls |
| legendary.mp3 | Legendary Pokémon animation |
| chaching.mp3 | When legendary is revealed |
| gotemall.mp3 | Collection complete (plays once) |

### Volume Levels

- Background Music: 25%
- Sound Effects: 35%

---

## 🎬 Animations

### Gacha Animation

Duration: 1.5-2.0 seconds (scales with rarity)

**Effects Applied**:
1. **Shake**: Horizontal/vertical offset based on rarity
2. **Rotation**: Slight rotation effect (increases with rarity)
3. **Color Tint**: Colorized by rarity
4. **Rays Background**: 
   - Scales by rarity (1.25x - 2.5x)
   - Color-tinted by rarity
   - Rotates continuously

**10-Pull Animations**:
- Individual animations for each Pokémon
- Staggered timing (wave effect)
- Individual rays behind each Pokémon
- Scaled appropriately for grid layout

**Skip**: Click anywhere to skip animation

### Rarity Animation Intensity

| Rarity | Shake | Rotation | Rays Scale | Tint Alpha |
|--------|-------|----------|------------|------------|
| Common | Low | Minimal | 1.25x | 100 |
| Uncommon | Low | Minimal | 1.5x | 130 |
| Rare | Medium | Medium | 1.75x | 160 |
| Epic | High | High | 2.0x | 200 |
| Legendary | Extreme | Extreme | 2.5x | 255 |

---

## 💰 Pokédollar System

### Earning Pokédollars

- **Click Currency**: Click Pokédollar display to add 10,000
- **Hold Click**: Hold to continuously add 10,000 every 0.1s
- **Add Money Button**: In insufficient funds popup (+20,000)

### Currency Display

- **Icon**: Pokédollar symbol
- **Format**: Comma-separated (e.g., 123,456)
- **Background**: Dark gray container with border
- **Locations**: Pokédex, Gacha Buy, Gacha Outcome

### Costs

| Action | Cost |
|--------|------|
| Red/Blue 1-Pull | 1,000 |
| Red/Blue 10-Pull | 9,000 (10% discount) |
| Yellow 1-Pull | 1,500 |
| Yellow 10-Pull | 13,500 (10% discount) |

---

## 💾 Save System

### Auto-Save

Game automatically saves after:
- Gacha pulls
- Gold/Pokédollar changes
- Music mute toggle
- Inventory reset

### Saved Data

- Pokédollar balance
- Pokémon owned (with counts)
- Newly acquired flags (for NEW badges)
- Pull statistics (total and per-machine)
- Music mute state
- Collection complete sound flag

### Save Location

`saves/savegame.json`

### Reset

- **Reset Button**: Clears inventory and pull statistics
- **No Confirmation**: Immediate action
- **Gold Preserved**: Pokédollars not affected

---

## 🎨 Visual Design

### Pokémon Tiles

- **Sprite**: Centered Pokémon image
- **Type Icons**: Top-left, stacked vertically
- **Count**: Bottom-right, large and prominent
- **Background**: Primary type color (or gray if unowned)
- **Outline**: Rarity color with glow
- **NEW Badge**: Top-right, large yellow badge

### Color Schemes

**Types**: Each of 15 types has unique color
**Rarities**:
- Common: White (#FFFFFF)
- Uncommon: Green (#1EFF00)
- Rare: Blue (#0070DD)
- Epic: Purple (#A335EE)
- Legendary: Orange (#FF8000)

### UI Polish

- Hover effects on all buttons
- Smooth scrolling
- Semi-transparent overlays for popups
- Responsive button states
- Proper spacing and alignment

---

## ⌨️ Controls

### Mouse

- **Click**: Activate buttons, select machines
- **Mouse Wheel**: Scroll Pokédex and lists
- **Click Currency**: Add Pokédollars
- **Hold Currency**: Continuously add Pokédollars
- **Click Anywhere**: Skip animations

### Keyboard

- **ESC**: Close popups

---

## 🎯 Tips & Strategies

### Optimal Collection Strategy

1. **Early Game**: Use Red/Blue for common Pokémon
2. **Mid Game**: Switch between machines for exclusives
3. **Late Game**: Focus on Yellow for legendaries (2x rate)
4. **Check Stats**: Use INFO panel to see which machine needs most pulls
5. **Follow Recommendation**: Badge shows optimal machine

### Expected Costs

Based on optimal strategy:
- Complete collection: ~300,000-400,000 Pokédollars
- All legendaries: ~150,000-200,000 Pokédollars (Yellow machine)
- Single version exclusive: ~50,000-100,000 Pokédollars

### Efficiency Tips

- Always use 10-pulls (10% discount)
- Check drop rates before pulling (INFO button)
- Use recommended machine badge
- Click optimal cost in stats to set your money

---

## 🐛 Known Limitations

- No online features (single-player only)
- No trading or battles
- No shiny variants
- No pity system (pure RNG)
- No daily bonuses

---

## 📱 Accessibility

- Large, readable fonts
- Clear visual feedback
- Color-coded with text labels
- Scrollable interfaces
- Skip options for animations
- Persistent settings

---

This guide covers all major features. For technical details, see `DEVELOPMENT_HISTORY.md`.

