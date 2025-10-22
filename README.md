# Pokémon Blue Gacha

A single-player desktop gacha game featuring all 151 Generation 1 Pokémon. Built with Python and Pygame.

## 🎮 Overview

Roll for Pokémon using three different gacha machines (Red, Blue, Yellow), each with unique pools and rates. Collect all 151 Pokémon and manage your Pokédex!

## ✨ Features

### Three Gacha Machines
- **Red Machine** (1,000 / 9,000 Pokédollars)
  - Red version exclusive Pokémon (Growlithe, Arcanine, Scyther, etc.)
- **Blue Machine** (1,000 / 9,000 Pokédollars)
  - Blue version exclusive Pokémon (Sandshrew, Vulpix, Pinsir, etc.)
- **Yellow Machine** (1,500 / 13,500 Pokédollars)
  - All Pokémon available
  - **2x Legendary drop rate**
  - 50% higher cost

### Pokédex System
- Full 151 Pokémon collection tracking
- Sort by: Number, Rarity, Amount Owned
- Filter: Show All / Owned Only
- Track duplicate counts
- "NEW!" badges for first-time catches
- Rarity-colored outlines with glow effects
- Type-colored backgrounds

### Gacha Statistics
- Track total pulls and per-machine pulls
- Expected pulls calculator (shows rarest Pokémon odds)
- Recommended machine badge (suggests best gacha to use)
- Optimal strategy cost calculator
- Complete collection from scratch estimates

### Drop Rate Transparency
- INFO button on gacha page shows all Pokémon and their exact drop rates
- Scrollable list with percentages
- Rarity color-coding for easy identification
- Version-specific rates displayed

### Audio System
- 8 background music tracks (randomly selected and shuffled)
- Change music by clicking Pokédollar display or unmuting
- Mute/unmute toggle (persists between sessions)
- Sound effects for pulls:
  - Common/Uncommon/Rare/Epic: Random roll sounds
  - Legendary: Special "cha-ching" sound
  - Collection complete: Special celebration sound

### Gacha Animations
- Shake, rotation, and color tint effects based on rarity
- Rays background effect (scaled and colored by rarity)
- Individual animations for each Pokémon in 10-pulls
- Skip animation by clicking

### Save System
- Auto-save progress (Pokédollars, Pokémon, statistics)
- Persistent music mute state
- Collection complete sound flag (plays once)
- JSON-based save file

## 🎯 Game Flow

1. **Loading State**: Splash screen with logo background
2. **Pokédex State**: View collection, access gacha, view stats
3. **Gacha Buy State**: Select machine, view featured Pokémon, purchase pulls
4. **Gacha Animation State**: Watch the rolls with effects
5. **Gacha Outcome State**: View results, pull again, or return to Pokédex

## 🎲 Gacha Mechanics

### Two-Step Weighted System
1. **Step 1**: Roll for rarity tier (based on rarity weights)
2. **Step 2**: Roll for specific Pokémon within that rarity (based on Pokémon weights)

### Rarity Tiers
- **Common** (White) - 42% base drop rate
- **Uncommon** (Green) - 36% base drop rate
- **Rare** (Blue) - 15% base drop rate
- **Epic** (Purple) - 6% base drop rate
- **Legendary** (Orange) - 1% base drop rate (2% in Yellow)

### Pull Options
- **1-Pull**: Single Pokémon roll
- **10-Pull**: 10 Pokémon rolls with 10% discount

## 📊 Data Files

Located in `data/` folder:
- `pokemon_gen1.csv` - All 151 Pokémon with types, rarities, version-specific weights
- `pokemon_types.csv` - 15 types with icons and colors
- `rarity_drop_weights.csv` - 5 rarity tiers with version-specific weights and colors
- `gacha_machines.csv` - 3 machine definitions with costs and descriptions

## 🎨 Assets

### Images
- Pokémon sprites: `Assets/Sprites/Pokemon/`
- Type icons: `Assets/Sprites/Types/`
- UI elements: `Assets/Sprites/Main/`
  - Gacha machine images (Red, Blue, Yellow)
  - Logo
  - Pokédollar icon
  - Rays effect

### Fonts
- `Assets/Font/8BitFont.ttf` - Body text
- `Assets/Font/TitleFont.ttf` - Titles and headers

### Audio
- Background music: `Assets/Sounds/background1-8.mp3`
- Sound effects: `Assets/Sounds/` (roll1-3, legendary, chaching, gotemall)

## 🚀 Installation & Running

### Requirements
- Python 3.7+
- Pygame

### Setup
```bash
# Install dependencies
pip install pygame

# Run the game
python src/main.py
```

## 🎮 Controls

- **Mouse**: Click buttons, scroll lists
- **Mouse Wheel**: Scroll Pokédex and drop rate lists
- **Click Pokédollar**: Add 10,000 (hold for continuous)
- **ESC**: Close popups

## 💡 Tips

1. **Yellow Machine**: Best for legendaries (2x rate)
2. **Red/Blue Machines**: Use for version exclusives
3. **Stats Panel**: Check recommendations for optimal pulls
4. **Drop Rates**: Click INFO to see exact percentages
5. **Music**: Click Pokédollar icon to change tracks

## 🏗️ Project Structure

```
PokemonBlueGacha/
├── src/
│   ├── main.py                 # Entry point
│   ├── config.py               # Game constants
│   ├── data/                   # Data classes
│   ├── managers/               # Core managers
│   ├── states/                 # Game states
│   ├── ui/                     # UI components
│   └── utils/                  # Utility functions
├── data/                       # CSV data files
├── Assets/                     # Images, fonts, sounds
├── saves/                      # Player save files
└── Documentation/              # Additional docs
```

## 📝 Documentation

Additional documentation available in:
- `Documentation/GACHA_SYSTEM_SUMMARY.md` - Gacha system overview
- `Documentation/gacha_system_logic.md` - Detailed gacha logic
- `Documentation/ASSETS_SUMMARY.md` - Asset creation guide

Recent feature documentation:
- `RANDOM_MUSIC_SYSTEM.md` - Music system details
- `GACHA_INFO_POPUP_FEATURE.md` - Drop rate display
- `STATS_AND_RECOMMENDATIONS_FEATURE.md` - Statistics panel

## 🎉 Special Features

- **Collection Complete Sound**: Plays once when you catch all 151
- **Legendary Cha-Ching**: Special sound for legendary pulls
- **Persistent Preferences**: Music mute state saved between sessions
- **Smart Recommendations**: Game suggests which machine to use
- **Optimal Strategy Cost**: Calculates expected Pokédollars to complete collection
- **Clickable Optimal Cost**: Click the cost in stats to set your money to that amount

## 🔄 Version History

- **v1.0**: Initial release with basic gacha system
- **v1.1**: Added three-machine system (Red/Blue/Yellow)
- **v1.2**: Enhanced Pokédex with sort/filter options
- **v1.3**: Added statistics and recommendations
- **v1.4**: Implemented drop rate transparency (INFO button)
- **v1.5**: 8-track random music system
- **Current**: Fully featured with animations, sound effects, and polish

## 📄 License

This is a fan project for educational purposes. Pokémon and all related properties are owned by Nintendo, Game Freak, and The Pokémon Company.

## 🙏 Credits

- Pokémon sprites and data from various community databases
- Background music and sound effects sourced for educational use
- Built with Python and Pygame
