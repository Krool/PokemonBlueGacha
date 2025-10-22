# 🎮 Pokémon Blue Gacha

<div align="center">

A fully-featured browser-based gacha collection game featuring all 151 Generation 1 Pokémon plus 79 classic items!

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-green?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Complete-success)
![Web](https://img.shields.io/badge/Web-Ready-orange)

**[▶️ Play in Browser](https://USERNAME.github.io/PokemonBlueGacha/)** *(Update USERNAME with your GitHub username)*

*No installation required! Works on desktop and mobile browsers.*

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Gameplay Guide](#-gameplay-guide)
- [Gacha System](#-gacha-system)
- [Project Architecture](#-project-architecture)
- [Installation](#-installation)
- [Web Deployment](#-web-deployment)
- [Configuration](#-configuration)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🎰 Four Unique Gacha Machines

| Machine | Cost (1-Pull / 10-Pull) | Special Features |
|---------|------------------------|------------------|
| **Red Machine** | 1,000₽ / 9,000₽ | Red version exclusives (Growlithe, Arcanine, Scyther, etc.) |
| **Blue Machine** | 1,000₽ / 9,000₽ | Blue version exclusives (Sandshrew, Vulpix, Pinsir, etc.) |
| **Yellow Machine** | 1,500₽ / 13,500₽ | **ALL Pokémon + 2x legendary rate!** (50% price premium) |
| **Items Machine** | 1,000₽ / 9,000₽ | 79 valuable Gen 1 items (Master Ball, Rare Candy, TMs, etc.) |

### 📖 Complete Pokédex System
- **151 Gen 1 Pokémon** - Complete first generation
- **Interactive Grid** - Visual collection tracker
- **Multiple Sort Options** - By number, rarity, or quantity
- **Filter System** - Show owned only or all Pokémon
- **Rarity Indicators** - Color-coded borders for each tier
- **NEW! Badges** - Highlight first-time acquisitions
- **Type Icons** - Dual-type Pokémon properly displayed
- **Progress Tracking** - Real-time collection completion percentage

### 💰 Advanced Economy System
- **Pokédollar Currency** - Authentic Pokémon economy
- **Click-to-Add Money** - Quick testing and balance management
- **Strategic Pricing** - Different costs reward smart choices
- **10-Pull Discount** - Save 10% on bulk purchases
- **Expected Value Display** - Transparent item gacha economics

### 📊 Statistics & Analytics
- **Pull History** - Track total pulls by machine
- **Expected Pulls Calculator** - Uses Coupon Collector Problem math
- **Optimal Strategy Recommendations** - AI-powered gacha suggestions
- **Drop Rate Transparency** - View exact percentages for every outcome
- **Collection Progress** - Detailed completion metrics
- **From-Scratch Analysis** - Theoretical minimums for completion

### 🎨 Polished UI/UX
- **Beautiful Sprite-Based UI** - Authentic Pokémon aesthetics
- **Smooth Animations** - Rarity-based effects and transitions
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Touch Controls** - Full mobile browser support
- **Hover Effects** - Interactive button feedback
- **Scrollable Grids** - Mouse wheel and touch scrolling

### 🎵 Dynamic Audio System
- **8 Background Tracks** - Randomized music rotation
- **Smart Music Changes** - New track on unmute or currency click
- **Sound Effects**:
  - Roll sounds for pulls (random selection)
  - Special legendary reveal sound
  - "Cha-ching" for rare acquisitions
  - Collection complete fanfare
- **Persistent Mute** - Preference saved between sessions
- **Browser-Compatible** - Handles autoplay policies gracefully

### 💾 Persistent Save System
- **Auto-Save** - Never lose your progress
- **Browser Storage** - IndexedDB for web builds
- **JSON Format** - Human-readable save files
- **Comprehensive Tracking**:
  - Pokédollar balance
  - Pokémon collection with counts
  - Item inventory with quantities
  - Pull statistics per machine
  - NEW flags for badges
  - Audio preferences
  - Collection milestones

---

## 🚀 Quick Start

### Play in Browser (Recommended)

**No installation needed!** Just visit the web version:
```
https://USERNAME.github.io/PokemonBlueGacha/
```

### Run Locally (Desktop)

```bash
# Clone the repository
git clone https://github.com/USERNAME/PokemonBlueGacha.git
cd PokemonBlueGacha

# Install dependencies
pip install pygame

# Run the game
python src/main.py
```

### Test Web Build Locally

```bash
# Install Pygbag
pip install pygbag

# Run in browser at http://localhost:8000
pygbag .
```

---

## 🎮 Gameplay Guide

### Getting Started

1. **Start with Pokédollars**
   - Click the currency display to add 10,000₽
   - Hold to continuously add money

2. **Open the Gacha**
   - Click "OPEN GACHA" from your Pokédex
   - Select one of four machines

3. **Choose Your Strategy**
   - Check the **INFO** button for drop rates
   - Look for the **RECOMMENDED** badge
   - Compare costs and benefits

4. **Pull and Collect**
   - Choose 1-pull or 10-pull
   - Watch the rarity-based animation
   - Celebrate your acquisitions!

5. **Complete Your Collection**
   - Collect all 151 Pokémon
   - Gather all 79 items
   - Track progress with statistics

### Pro Tips 💡

- **Yellow Machine** has 2x legendary rates but costs 50% more
- **10-pulls** always save 10% compared to single pulls
- Check **Statistics** to see which machine needs the most pulls
- **Pull Again** button remembers your machine and pull type
- Click **Pokédollar icon** to change background music
- Use the **INFO** popup to study drop rates before pulling
- The **RECOMMENDED** badge shows the most efficient machine

### Controls

#### Desktop
- **Mouse**: Click buttons, scroll with wheel
- **ESC**: Close popups
- **Click Currency**: Add money / change music

#### Mobile
- **Tap**: Activate buttons
- **Swipe**: Scroll through Pokédex
- **Tap Currency**: Add money / change music

---

## 🎲 Gacha System

### Two-Step Weighted Roll System

The game uses a sophisticated two-tier gacha system:

```
1. RARITY ROLL → Determine tier (Common, Uncommon, Rare, Epic, Legendary)
                 Uses rarity weights from rarity_drop_weights.csv
                 
2. ENTITY ROLL → Select specific Pokémon/Item within that rarity
                 Uses individual weights from pokemon_gen1.csv or items_gen1.csv
```

This ensures:
- ✅ Accurate rarity distribution
- ✅ Individual entity weight adjustments
- ✅ Transparent probability calculations
- ✅ Event-ready system for featured rates

### Drop Rates by Machine

#### Pokémon Machines (Red/Blue)
| Rarity | Probability | Example Pokémon |
|--------|-------------|-----------------|
| Common | 42% | Caterpie, Pidgey, Rattata |
| Uncommon | 36% | Starter evolutions, Eevee |
| Rare | 15% | Pikachu, Dratini, Lapras |
| Epic | 6% | Final starter forms, Snorlax |
| Legendary | 1% | Articuno, Zapdos, Moltres, Mewtwo, Mew |

#### Yellow Machine (Special)
| Rarity | Probability | Notes |
|--------|-------------|-------|
| Common | 41% | -1% to compensate for legendary boost |
| Uncommon | 36% | Unchanged |
| Rare | 15% | Unchanged |
| Epic | 6% | Unchanged |
| Legendary | **2%** | **DOUBLE the standard rate!** |

#### Items Machine
| Rarity | Probability | Example Items |
|--------|-------------|--------------|
| Common | 42% | Potions, Antidotes, Basic TMs |
| Uncommon | 36% | Full Restore, Max Potion, Revive |
| Rare | 15% | Evolution Stones, Ice Beam TM |
| Epic | 6% | Earthquake TM, HP Up, Protein |
| Legendary | 1% | **Master Ball**, Rare Candy |

### Version Exclusives

#### Red Machine Only
- Oddish, Gloom, Vileplume
- Mankey, Primeape
- Growlithe, Arcanine
- Scyther, Electabuzz

#### Blue Machine Only
- Sandshrew, Sandslash
- Vulpix, Ninetales
- Meowth, Persian
- Bellsprout, Weepinbell, Victreebel
- Magmar, Pinsir

#### Yellow Machine
- **ALL 151 Pokémon available**
- Best for completing your collection
- 2x legendary rate justifies the premium cost

### Expected Pulls Mathematics

The game uses the **Coupon Collector Problem** to calculate:

```
E[pulls] ≈ Σ(1/p_i) for all unowned Pokémon i

where p_i = P(rarity) × P(pokémon | rarity)
```

This provides accurate estimates for:
- Pulls needed per machine
- Optimal strategy selection
- From-scratch completion estimates
- Cost projections

---

## 🏗️ Project Architecture

### Tech Stack

- **Language**: Python 3.11+
- **Framework**: Pygame 2.6+
- **Web Deployment**: Pygbag (Python → WebAssembly)
- **Data Format**: CSV (easy to modify)
- **Save Format**: JSON (human-readable)
- **Assets**: PNG sprites, MP3 audio

### Project Structure

```
PokemonBlueGacha/
├── src/
│   ├── main.py                      # Entry point (async-ready)
│   ├── config.py                    # Configuration constants
│   │
│   ├── managers/                    # Core management systems
│   │   ├── audio_manager.py         # Sound & music handling
│   │   ├── font_manager.py          # Font loading & caching
│   │   ├── game_data.py             # Game state & inventory
│   │   ├── resource_manager.py      # Asset loading & caching
│   │   ├── save_manager.py          # Save/load system
│   │   └── state_manager.py         # State machine coordinator
│   │
│   ├── states/                      # Game state implementations
│   │   ├── base_state.py            # Abstract base class
│   │   ├── loading_state.py         # Asset loading screen
│   │   ├── inventory_state.py       # Pokédex/collection view
│   │   ├── gacha_buy_state.py       # Machine selection & purchase
│   │   ├── gacha_animation_state.py # Roll animation & reveal
│   │   └── gacha_outcome_state.py   # Results display
│   │
│   ├── ui/                          # Reusable UI components
│   │   ├── button.py                # Interactive buttons
│   │   ├── checkbox.py              # Toggle checkboxes
│   │   ├── currency_display.py      # Pokédollar counter
│   │   ├── pokemon_tile.py          # Pokémon grid item
│   │   ├── item_tile.py             # Item grid item
│   │   ├── scrollable_grid.py       # Scrolling container
│   │   ├── sort_button.py           # Multi-state sort buttons
│   │   ├── popup.py                 # Modal dialog base
│   │   ├── gacha_info_popup.py      # Drop rates display
│   │   ├── items_info_popup.py      # Item rates display
│   │   └── stats_popup.py           # Statistics display
│   │
│   ├── logic/                       # Core game logic
│   │   ├── gacha_logic.py           # Pokémon gacha system
│   │   └── items_gacha.py           # Items gacha system
│   │
│   ├── data/                        # Data structures & loaders
│   │   ├── csv_loader.py            # CSV parsing utilities
│   │   ├── pokemon_data.py          # Pokémon class
│   │   ├── item_data.py             # Item class
│   │   ├── rarity_data.py           # Rarity class
│   │   ├── type_data.py             # Type class
│   │   ├── gacha_machine_data.py    # Machine definitions
│   │   ├── pokemon_gen1.csv         # 151 Pokémon database
│   │   ├── items_gen1.csv           # 79 items database
│   │   ├── pokemon_types.csv        # 15 type definitions
│   │   ├── rarity_drop_weights.csv  # Rarity tier weights
│   │   └── gacha_machines.csv       # Machine configurations
│   │
│   ├── utils/                       # Utility modules
│   │   └── gacha_stats.py           # Statistics calculations
│   │
│   └── Assets/                      # Game assets
│       ├── Sprites/
│       │   ├── Pokemon/             # 151 Pokémon sprites (56x56)
│       │   ├── Items/               # 79 item icons (32x32)
│       │   ├── Types/               # 15 type icons
│       │   └── Main/                # UI elements (logos, machines)
│       ├── Sounds/                  # Sound effects (MP3)
│       │   ├── roll1.mp3, roll2.mp3, roll3.mp3
│       │   ├── legendary.mp3, chaching.mp3
│       │   ├── gotemall.mp3
│       │   └── click1.mp3, click2.mp3, click3.mp3
│       ├── Music/                   # Background tracks
│       │   └── background1.mp3 - background8.mp3 (8 tracks)
│       └── Font/
│           ├── TitleFont.ttf        # Header font
│           └── 8BitFont.ttf         # Body font
│
├── docs/                            # Comprehensive documentation
│   ├── DEVELOPMENT_HISTORY.md       # Project timeline
│   ├── FEATURES.md                  # Detailed feature guide
│   ├── GACHA_SYSTEM_SUMMARY.md      # Gacha math & logic
│   ├── WEB_DEPLOYMENT_GUIDE.md      # Deployment instructions
│   ├── THREE_GACHA_SYSTEM.md        # Multi-machine system
│   ├── ITEMS_GACHA_COMPLETE.md      # Items implementation
│   ├── STATS_AND_RECOMMENDATIONS.md # Analytics system
│   └── ... (30+ documentation files)
│
├── scripts/                         # Development utilities
│   ├── download_pokemon_images.py   # Asset scraping
│   ├── download_item_icons.py       # Item icon fetching
│   ├── gacha_calculations.py        # Probability calculator
│   └── ...
│
├── saves/                           # Save file directory
│   └── player_save.json             # Auto-generated save
│
├── index.html                       # Web build template
├── requirements.txt                 # Python dependencies
├── LICENSE                          # MIT License
└── README.md                        # This file
```

### Design Patterns

#### State Machine Pattern
- Clean separation of game screens
- Easy state transitions
- Managed by `StateManager`

#### Manager Pattern
- `ResourceManager`: Asset loading & caching
- `SaveManager`: Persistence layer
- `GameData`: Game state & inventory
- `AudioManager`: Sound system
- `FontManager`: Font rendering

#### Component-Based UI
- Reusable UI components
- Event-driven architecture
- Modular and testable

#### Data-Driven Design
- All game data in CSV files
- Easy to modify and balance
- No code changes for content updates

---

## 💻 Installation

### Prerequisites

- **Python 3.11 or higher**
- **pip** (Python package manager)

### Desktop Installation

```bash
# 1. Clone the repository
git clone https://github.com/USERNAME/PokemonBlueGacha.git
cd PokemonBlueGacha

# 2. Install Pygame
pip install pygame

# 3. Run the game
python src/main.py
```

### Web Testing (Local)

```bash
# 1. Install Pygbag
pip install pygbag

# 2. Run local web server
pygbag .

# 3. Open browser to http://localhost:8000
```

### Dependencies

```txt
pygame>=2.6.0      # Game framework
pygbag>=0.9.0      # Web deployment (optional)
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🌐 Web Deployment

### Deploy to GitHub Pages (FREE!)

#### Step 1: Build for Web
```bash
pygbag --build .
```

#### Step 2: Create GitHub Repository
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/PokemonBlueGacha.git
git push -u origin main
```

#### Step 3: Deploy Build Files

**Option A: Use `docs` folder**
```bash
mkdir docs
cp -r build/web/* docs/
git add docs
git commit -m "Add web build"
git push
```

Then on GitHub:
1. Go to **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** → folder: **/docs**
4. Save

**Option B: Use `gh-pages` branch**
```bash
git checkout -b gh-pages
cp -r build/web/* .
git add .
git commit -m "Deploy to GitHub Pages"
git push -u origin gh-pages
```

Then on GitHub:
1. Go to **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **gh-pages** → folder: **/ (root)**
4. Save

Your game will be live at: `https://YOUR_USERNAME.github.io/PokemonBlueGacha/`

### Deploy to Itch.io (FREE!)

```bash
# 1. Build
pygbag --build .

# 2. Create ZIP
cd build/web
zip -r ../../PokemonBlueGacha.zip *
cd ../..

# 3. Upload to Itch.io
# Visit https://itch.io/game/new
# Upload PokemonBlueGacha.zip as HTML game
```

### Browser Compatibility

✅ Chrome 66+  
✅ Firefox 66+  
✅ Safari 11+  
✅ Edge 79+ (Chromium)  
✅ Mobile Chrome/Safari  
✅ iPad/Tablet browsers  

**Note**: First click required for audio (browser security policy)

---

## ⚙️ Configuration

### Game Settings (`src/config.py`)

```python
# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Starting balance
STARTING_GOLD = 0
GOLD_CHEAT_AMOUNT = 10000  # Click currency to add

# Animation settings
MAX_ANIMATION_TIME = 2.0   # seconds
LOADING_TIME = 4.0         # seconds
```

### Gacha Machine Costs (`data/gacha_machines.csv`)

| Machine | Single Pull | 10-Pull | Discount |
|---------|-------------|---------|----------|
| Red | 1,000₽ | 9,000₽ | 10% |
| Blue | 1,000₽ | 9,000₽ | 10% |
| Yellow | 1,500₽ | 13,500₽ | 10% |
| Items | 1,000₽ | 9,000₽ | 10% |

### Rarity Weights (`data/rarity_drop_weights.csv`)

Adjust drop rates by modifying weights:

```csv
Rarity,Red_Weight,Blue_Weight,Yellow_Weight,Items_Weight
Common,42,42,41,42
Uncommon,36,36,36,36
Rare,15,15,15,15
Epic,6,6,6,6
Legendary,1,1,2,1
```

### Individual Pokémon Weights (`data/pokemon_gen1.csv`)

Set `Red_Weight`, `Blue_Weight`, `Yellow_Weight` to adjust individual rates:
- `0` = Not available in that version
- `1` = Standard rate (default)
- `2+` = Increased rate (featured Pokémon)

### Audio Settings (`src/managers/audio_manager.py`)

```python
# Volume levels
MUSIC_VOLUME = 0.5      # 50%
SOUND_VOLUME = 0.35     # 35%

# Number of audio channels
NUM_CHANNELS = 8
```

---

## 📚 Documentation

### Core Documentation Files

- **[DEVELOPMENT_HISTORY.md](docs/DEVELOPMENT_HISTORY.md)** - Complete project timeline
- **[FEATURES.md](docs/FEATURES.md)** - Detailed feature descriptions
- **[GACHA_SYSTEM_SUMMARY.md](docs/GACHA_SYSTEM_SUMMARY.md)** - Mathematics & logic
- **[WEB_DEPLOYMENT_GUIDE.md](docs/WEB_DEPLOYMENT_GUIDE.md)** - Deployment instructions
- **[THREE_GACHA_SYSTEM.md](docs/THREE_GACHA_SYSTEM.md)** - Multi-machine architecture

### Specialized Guides

- **Items Gacha**: `ITEMS_GACHA_COMPLETE.md`, `ITEMS_GACHA_IMPLEMENTATION_COMPLETE.md`
- **Statistics System**: `STATS_AND_RECOMMENDATIONS_FEATURE.md`
- **Audio System**: `AUDIO_SYSTEM_FIXES.md`, `RANDOM_MUSIC_SYSTEM.md`
- **Web Conversion**: `WEB_CONVERSION_SUMMARY.md`, `ASYNC_CONVERSION_COMPLETE.md`

### Development Scripts

Located in `scripts/`:
- `download_pokemon_images.py` - Scrape Pokémon sprites
- `download_item_icons.py` - Fetch item icons
- `gacha_calculations.py` - Probability calculator
- `gacha_weight_example.py` - Weight system examples

---

## 🎯 Roadmap

### Completed ✅
- [x] Complete Gen 1 Pokémon collection (151)
- [x] Four gacha machines (Red, Blue, Yellow, Items)
- [x] Items gacha with 79 items
- [x] Statistics and recommendations system
- [x] Drop rate transparency
- [x] Save/load system
- [x] Audio system (8 tracks + sound effects)
- [x] Web deployment ready
- [x] Mobile browser support
- [x] Complete documentation

### Future Ideas 💭
- [ ] Generation 2 Pokémon (251 total)
- [ ] Shiny variants (rare alternate colors)
- [ ] Trading system (local multiplayer)
- [ ] Daily login bonuses
- [ ] Achievement system
- [ ] Leaderboards
- [ ] Item usage system (apply to Pokémon)
- [ ] Pokémon battles
- [ ] Evolution mechanics
- [ ] Additional gacha machines

**Want to contribute?** Open an issue or pull request!

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs 🐛
1. Check if the bug is already reported in [Issues](https://github.com/USERNAME/PokemonBlueGacha/issues)
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

### Suggesting Features 💡
1. Open a [Feature Request](https://github.com/USERNAME/PokemonBlueGacha/issues/new)
2. Describe the feature
3. Explain why it would be useful
4. Provide examples if possible

### Submitting Pull Requests 🔧

```bash
# 1. Fork the repository
# 2. Create a feature branch
git checkout -b feature/amazing-feature

# 3. Make your changes
# 4. Test thoroughly
python src/main.py  # Desktop test
pygbag .           # Web test

# 5. Commit with clear messages
git commit -m "Add amazing feature"

# 6. Push to your fork
git push origin feature/amazing-feature

# 7. Open a Pull Request
```

### Development Guidelines

- **Code Style**: Follow PEP 8
- **Documentation**: Update relevant docs
- **Testing**: Test both desktop and web builds
- **Comments**: Write clear, helpful comments
- **Commits**: Use descriptive commit messages

### Areas Needing Help

- 🎨 Additional sprites/assets
- 🌍 Translations/localization
- 📱 Mobile UX improvements
- 🎵 Additional music tracks
- 📖 Tutorial system
- ⚡ Performance optimizations

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### TL;DR

✅ Free to use  
✅ Free to modify  
✅ Free to distribute  
✅ Private and commercial use OK  
⚠️ Keep the license and copyright notice  

---

## 📜 Disclaimer

**This is an unofficial fan-made game.**

Pokémon © 1995-2025 Nintendo / Game Freak / Creatures Inc. / The Pokémon Company

This project is **not affiliated with, endorsed by, or connected to** Nintendo, Game Freak, The Pokémon Company, or any official Pokémon entities.

All Pokémon names, sprites, types, and related intellectual property are trademarks and copyrights of their respective owners.

This game is provided **free of charge** for educational and entertainment purposes only. No profit is made from this project.

---

## 🙏 Acknowledgments

### Core Technologies
- **[Pygame](https://www.pygame.org/)** - Python game development framework
- **[Pygbag](https://pygame-web.github.io/)** - Python to WebAssembly compiler
- **[Python](https://www.python.org/)** - Programming language

### Data Sources
- **[PokéAPI](https://pokeapi.co/)** - Pokémon data API
- **[Bulbapedia](https://bulbapedia.bulbagarden.net/)** - Pokémon encyclopedia
- **[Serebii.net](https://www.serebii.net/)** - Pokémon database
- **[PokéSprite](https://msikma.github.io/pokesprite/)** - Pokémon sprite collection

### Assets
- **Nintendo/Game Freak** - Original Pokémon games and artwork
- Sprite artists and contributors from the Pokémon community

### Community
- Pygame community for excellent documentation and support
- Contributors and testers who helped improve the game
- Players who provided valuable feedback

---

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/USERNAME/PokemonBlueGacha/issues)
- **GitHub Discussions**: [Ask questions or share ideas](https://github.com/USERNAME/PokemonBlueGacha/discussions)
- **Pull Requests**: [Contribute code](https://github.com/USERNAME/PokemonBlueGacha/pulls)

---

## 📊 Project Statistics

- **Total Lines of Code**: ~8,000+
- **Python Files**: 30+
- **Pokémon**: 151 (Generation 1)
- **Items**: 79 (Generation 1)
- **Gacha Machines**: 4
- **Rarity Tiers**: 5
- **Pokémon Types**: 15
- **Background Music Tracks**: 8
- **Sound Effects**: 6+
- **Game States**: 5
- **UI Components**: 10+
- **CSV Data Files**: 5
- **Documentation Files**: 30+
- **Development Time**: 100+ hours
- **Current Status**: ✅ **Complete & Playable**

---

## ⭐ Star History

If you enjoy this game, please consider starring the repository! It helps others discover the project.

[![Star History Chart](https://api.star-history.com/svg?repos=USERNAME/PokemonBlueGacha&type=Date)](https://star-history.com/#USERNAME/PokemonBlueGacha&Date)

---

<div align="center">

### Made with ❤️ and Python

**[Play Now](https://USERNAME.github.io/PokemonBlueGacha/)** • **[Report Bug](https://github.com/USERNAME/PokemonBlueGacha/issues)** • **[Request Feature](https://github.com/USERNAME/PokemonBlueGacha/issues)** • **[Documentation](docs/)**

---

*"Gotta catch 'em all!"* 🎮✨

</div>
