# 📁 Pokémon Blue Gacha - File Structure

**Last Updated:** After cleanup - October 2025

## 🎯 Directory Layout (Web-First Architecture)

```
PokemonBlueGacha/
├── src/                           # ← PRIMARY: All game code & assets
│   ├── main.py                    # Entry point (async for web)
│   ├── config.py                  # Platform detection & paths
│   │
│   ├── Assets/                    # ← All game assets (packaged in web)
│   │   ├── Sprites/
│   │   │   ├── Pokemon/           # 151 Pokémon sprites
│   │   │   ├── Items/             # 79 item icons
│   │   │   ├── Types/             # 15 type badges
│   │   │   └── Main/              # UI elements (gacha machines, logo, etc)
│   │   ├── Sounds/                # 14 audio files (8 music + 6 SFX)
│   │   └── Font/                  # TitleFont.ttf, 8BitFont.ttf
│   │
│   ├── data/                      # ← Game data (CSVs + loader classes)
│   │   ├── pokemon_gen1.csv       # 151 Pokémon definitions
│   │   ├── items_gen1.csv         # 79 items definitions
│   │   ├── gacha_machines.csv     # 4 gacha machine configs
│   │   ├── pokemon_types.csv      # Type definitions
│   │   ├── rarity_drop_weights.csv # Drop rate tables
│   │   ├── csv_loader.py          # CSV parsing & validation
│   │   ├── pokemon_data.py        # Pokemon dataclass
│   │   ├── item_data.py           # Item dataclass
│   │   ├── type_data.py           # Type dataclass
│   │   ├── rarity_data.py         # Rarity dataclass
│   │   └── gacha_machine_data.py  # Machine dataclass
│   │
│   ├── managers/                  # Core systems
│   │   ├── state_manager.py       # State machine controller
│   │   ├── resource_manager.py    # Asset loading & caching
│   │   ├── save_manager.py        # Save/Load (file + localStorage)
│   │   ├── game_data.py           # Player data wrapper
│   │   ├── audio_manager.py       # Music & SFX
│   │   └── font_manager.py        # Font loading
│   │
│   ├── states/                    # Game states
│   │   ├── base_state.py          # Abstract state class
│   │   ├── loading_state.py       # Initial loading screen
│   │   ├── inventory_state.py     # Pokédex/inventory view
│   │   ├── gacha_buy_state.py     # Machine selection & purchase
│   │   ├── gacha_animation_state.py # Pull animation
│   │   └── gacha_outcome_state.py # Results display
│   │
│   ├── logic/                     # Game logic
│   │   ├── gacha_logic.py         # Pokémon gacha system
│   │   └── items_gacha.py         # Items gacha system
│   │
│   ├── ui/                        # UI components
│   │   ├── button.py              # Clickable buttons
│   │   ├── checkbox.py            # Toggle checkbox
│   │   ├── currency_display.py    # Pokédollar counter
│   │   ├── pokemon_tile.py        # Pokédex entry display
│   │   ├── item_tile.py           # Item inventory entry
│   │   ├── scrollable_grid.py     # Scrollable grid container
│   │   ├── sort_button.py         # Sort/filter buttons
│   │   ├── popup.py               # Generic popup base
│   │   ├── gacha_info_popup.py    # Machine info & rates
│   │   ├── items_info_popup.py    # Item details popup
│   │   └── stats_popup.py         # Statistics & recommendations
│   │
│   ├── utils/                     # Utilities
│   │   └── gacha_stats.py         # Statistics calculations
│   │
│   ├── saves/                     # Desktop save files (auto-generated)
│   │   └── player_save.json       # (ignored in .gitignore)
│   │
│   └── build/                     # Pygbag build output (ignored in .gitignore)
│       └── web/
│           ├── index.html         # Web deployment entry
│           └── src.apk            # Packaged game (from src/)
│
├── scripts/                       # Development tools (not in web build)
│   ├── download_pokemon_images.py
│   ├── download_item_icons.py
│   ├── create_items_data.py
│   └── gacha_calculations.py
│
├── docs/                          # Documentation
│   ├── WEB_CONVERSION_SUMMARY.md
│   ├── GITHUB_PAGES_DEPLOYMENT.md
│   └── [28 other documentation files]
│
├── index.html                     # Web entry point (loads src.apk)
├── src.apk                        # Current web build (packaged src/)
├── favicon.png                    # Web favicon
├── README.md                      # Main documentation
├── .gitignore                     # Git exclusions
├── requirements.txt               # Python dependencies
└── PokemonBlueGacha.code-workspace # VS Code workspace
```

---

## 🌐 How It Works

### **Web Deployment (PRIMARY)**

1. **Build**: `pygbag --build .` (from project root)
   - Packages entire `src/` folder into `src.apk`
   - Creates `src/build/web/index.html` + `src.apk`
   
2. **Deploy**: Copy to web host
   - Files needed: `index.html` + `src.apk` + `favicon.png`
   - GitHub Pages, Itch.io, Netlify, etc.

3. **Runtime**:
   - Browser loads `index.html`
   - Pygbag loads `src.apk` into virtual filesystem
   - Runs `src/main.py` with `sys.platform = "emscripten"`
   - `config.py` detects `IS_WEB = True`
   - Paths resolve relative to mounted APK (e.g., `data/pokemon_gen1.csv`)
   - Saves to `localStorage` API

### **Python Standalone (SECONDARY)**

1. **Run**: `cd src && python main.py` (from project root)
   
2. **Runtime**:
   - Working directory: `C:\...\PokemonBlueGacha\src\`
   - `config.py` detects `IS_WEB = False`
   - `os.path.exists("data")` → `True`
   - `BASE_PATH = ""`
   - Paths resolve locally (e.g., `src/data/pokemon_gen1.csv`)
   - Saves to `src/saves/player_save.json`

---

## 🔧 Path Resolution Logic

```python
# config.py
IS_WEB = sys.platform == "emscripten"

def get_base_path():
    if IS_WEB or os.path.exists("data"):
        return ""  # We're in src/ or web mounted APK
    else:
        return "../"  # Edge case: running from elsewhere

BASE_PATH = get_base_path()
POKEMON_CSV = os.path.join(BASE_PATH, "data/pokemon_gen1.csv")
```

**Result:**
- Web: `data/pokemon_gen1.csv` (from mounted APK)
- Standalone: `data/pokemon_gen1.csv` (from local src/)

---

## ✅ What Was Fixed

### Before Cleanup
```
❌ /Assets/          248 files (duplicate)
❌ /data/            5 CSVs (duplicate)
❌ /saves/           duplicate save location
❌ Double storage    ~500+ duplicate files
❌ Confusing paths   which is source of truth?
```

### After Cleanup
```
✅ src/Assets/       248 files (single source)
✅ src/data/         5 CSVs (single source)
✅ src/saves/        desktop saves only
✅ Clean structure   no duplication
✅ Clear ownership   src/ is primary
```

---

## 📦 What Gets Packaged in Web Build

When `pygbag --build .` runs:

**Included in src.apk:**
- ✅ All `.py` files in `src/`
- ✅ `src/Assets/` (all sprites, sounds, fonts)
- ✅ `src/data/*.csv`
- ✅ Python packages/modules

**Excluded:**
- ❌ `src/saves/player_save.json` (uses localStorage instead)
- ❌ `src/__pycache__/` (bytecode ignored)
- ❌ `src/build/` (build output)
- ❌ Everything outside `src/` (scripts, docs, etc.)

---

## 🚀 Quick Commands

```bash
# Test web locally
pygbag .

# Build for web deployment
pygbag --build .

# Run Python standalone
cd src
python main.py

# Return to root
cd ..
```

---

## 💾 Save System

| Platform | Location | API |
|----------|----------|-----|
| **Web** | Browser localStorage | `window.localStorage.setItem()` |
| **Desktop** | `src/saves/player_save.json` | `json.dump(file)` |

Both use the same JSON structure for compatibility.

---

## 🎯 Best Practices

1. **Always work in src/**
   - All assets belong here
   - All code belongs here
   - Single source of truth

2. **Test both platforms**
   ```bash
   # Test web
   pygbag .
   
   # Test desktop
   cd src && python main.py
   ```

3. **Add new assets to src/Assets/**
   - Not root-level Assets/
   - They'll be packaged automatically

4. **Add new data to src/data/**
   - CSVs go here
   - Auto-loaded by csv_loader.py

5. **Use relative paths**
   - CSVs use: `Assets/Sprites/Pokemon/001_Bulbasaur.png`
   - Not absolute paths
   - config.py handles resolution

---

## 🔍 Verifying Structure

```bash
# Check paths work from src/
cd src
python -c "from config import *; print('POKEMON_CSV:', POKEMON_CSV); import os; print('Exists:', os.path.exists(POKEMON_CSV))"

# Should output:
# POKEMON_CSV: data/pokemon_gen1.csv
# Exists: True
```

---

## 📝 .gitignore Coverage

```gitignore
# Build artifacts (not committed)
src/build/
src.apk
*.apk

# Auto-generated saves (not committed)
src/saves/player_save.json

# Python cache (not committed)
__pycache__/
*.pyc
```

Root-level `index.html` and `src.apk` can optionally be committed for quick deployment.

---

## 🎓 Summary

- **Web-First**: Everything lives in `src/`
- **Clean**: No duplicate assets/data
- **Portable**: One codebase, two platforms
- **Scalable**: Easy to add content
- **Maintainable**: Single source of truth

All changes should be made in `src/` - they'll work on both web and desktop automatically! 🎉

