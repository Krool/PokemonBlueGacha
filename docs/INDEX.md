# Documentation Index

Complete guide to all documentation for Pokémon Blue Gacha.

## 📚 Essential Documentation

### For Players

- **[README.md](README.md)** - Main project overview, installation, and quick start
- **[FEATURES.md](FEATURES.md)** - Complete guide to all game features and mechanics

### For Developers

- **[DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md)** - Complete development timeline and lessons learned
- **[Documentation/](Documentation/)** - Technical documentation folder
  - **[GACHA_SYSTEM_SUMMARY.md](Documentation/GACHA_SYSTEM_SUMMARY.md)** - Gacha system overview
  - **[gacha_system_logic.md](Documentation/gacha_system_logic.md)** - Detailed gacha logic
  - **[ASSETS_SUMMARY.md](Documentation/ASSETS_SUMMARY.md)** - Asset creation guide

## 🎯 Feature-Specific Documentation

### Recent Features

- **[RANDOM_MUSIC_SYSTEM.md](RANDOM_MUSIC_SYSTEM.md)** - 8-track music system
- **[GACHA_INFO_POPUP_FEATURE.md](GACHA_INFO_POPUP_FEATURE.md)** - Drop rate transparency
- **[STATS_AND_RECOMMENDATIONS_FEATURE.md](STATS_AND_RECOMMENDATIONS_FEATURE.md)** - Statistics panel
- **[THREE_GACHA_SYSTEM.md](THREE_GACHA_SYSTEM.md)** - Three machine system

## 📂 Project Structure

```
PokemonBlueGacha/
├── README.md                   # Main documentation
├── FEATURES.md                 # Feature guide
├── DEVELOPMENT_HISTORY.md      # Development timeline
├── INDEX.md                    # This file
│
├── Documentation/              # Technical docs
│   ├── GACHA_SYSTEM_SUMMARY.md
│   ├── gacha_system_logic.md
│   └── ASSETS_SUMMARY.md
│
├── Feature Documentation/      # Specific features
│   ├── RANDOM_MUSIC_SYSTEM.md
│   ├── GACHA_INFO_POPUP_FEATURE.md
│   ├── STATS_AND_RECOMMENDATIONS_FEATURE.md
│   └── THREE_GACHA_SYSTEM.md
│
├── src/                        # Source code
│   ├── main.py
│   ├── config.py
│   ├── data/
│   ├── managers/
│   ├── states/
│   ├── ui/
│   └── utils/
│
├── data/                       # CSV data files
│   ├── pokemon_gen1.csv
│   ├── pokemon_types.csv
│   ├── rarity_drop_weights.csv
│   └── gacha_machines.csv
│
├── Assets/                     # Game assets
│   ├── Sprites/
│   ├── Font/
│   └── Sounds/
│
└── saves/                      # Player save files
    └── savegame.json
```

## 🎮 Quick Start Guide

1. **Installation**: See [README.md](README.md#installation--running)
2. **Features**: Read [FEATURES.md](FEATURES.md)
3. **Gameplay**: Launch game and enjoy!

## 🔧 Development Guide

1. **Architecture**: See [DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md#technical-highlights)
2. **Gacha Logic**: Read [Documentation/gacha_system_logic.md](Documentation/gacha_system_logic.md)
3. **Adding Features**: Follow existing patterns in `src/`

## 📊 Data Files

All CSV data files are in the `data/` folder:

- **pokemon_gen1.csv**: 151 Pokémon with types, rarities, weights
- **pokemon_types.csv**: 15 types with colors and icons
- **rarity_drop_weights.csv**: 5 rarity tiers with weights and colors
- **gacha_machines.csv**: 3 machines with costs and descriptions

## 🎨 Assets

All game assets are in the `Assets/` folder:

- **Sprites/Pokemon/**: 151 Pokémon sprites
- **Sprites/Types/**: 15 type icons
- **Sprites/Main/**: UI images (logo, gachas, icons)
- **Font/**: 8-bit and title fonts
- **Sounds/**: 8 music tracks + 6 sound effects

## 💾 Save System

Save file location: `saves/savegame.json`

Contains:
- Pokédollar balance
- Pokémon owned with counts
- Pull statistics
- Music mute state
- Collection complete flag

## 🐛 Troubleshooting

### Common Issues

**Game won't start:**
- Check Python version (3.7+)
- Install Pygame: `pip install pygame`
- Run from project root: `python src/main.py`

**Missing assets:**
- Ensure all files in `Assets/` folder
- Check file paths in `config.py`

**Save file issues:**
- Delete `saves/savegame.json` to reset
- Game will create new save on next launch

## 📝 Documentation Standards

When adding new features:

1. Update [FEATURES.md](FEATURES.md) with user-facing details
2. Update [DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md) with technical details
3. Create feature-specific doc if complex (see examples)
4. Update this INDEX.md with links

## 🎯 Next Steps

- **Playing the game?** → [README.md](README.md)
- **Learning features?** → [FEATURES.md](FEATURES.md)
- **Understanding code?** → [DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md)
- **Building features?** → [Documentation/](Documentation/)

---

**Last Updated**: Latest version with 8-track music system, drop rate transparency, and statistics panel.

**Documentation Status**: ✅ Complete and up-to-date

