# 🎮 Pokémon Blue Gacha

A browser-based gacha game featuring all 151 Generation 1 Pokémon plus 79 classic items!

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.6-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 🎯 Play Now

**[▶️ Play in Browser](https://USERNAME.github.io/PokemonBlueGacha/)** *(Update USERNAME with your GitHub username)*

No installation required! Works on desktop and mobile browsers.

---

## ✨ Features

### 🎰 Four Gacha Machines
- **Red Machine**: Red version exclusives + commons
- **Blue Machine**: Blue version exclusives + commons  
- **Yellow Machine**: All Pokémon + 2x legendary chance
- **Items Machine**: 79 valuable Gen 1 items

### 📖 Complete Pokédex
- Track all 151 Gen 1 Pokémon
- View by Pokédex number, rarity, or quantity
- Filter to show only owned Pokémon
- See rarity-colored borders and "NEW!" badges

### 💰 Smart Economy
- Earn Pokédollars for pulls
- Different costs for each machine type
- 1-pull and 10-pull options
- Strategic recommendations based on your collection

### 📊 Statistics & Analytics
- Track total pulls by machine
- Calculate expected pulls to completion
- View optimal gacha strategy
- See drop rates for all outcomes

### 🎨 Polish & UX
- Beautiful sprite-based UI
- Smooth animations with rarity effects
- 8 randomized background music tracks
- Sound effects for special moments
- Responsive design for mobile

### 💾 Persistent Saves
- Automatic save system
- Saves to browser storage (web)
- Saves to JSON file (desktop)
- Never lose your collection!

---

## 🎮 How to Play

1. **Start with Pokédollars**: Click the currency display to add money
2. **Open Gacha**: Click "OPEN GACHA" from your Pokédex
3. **Choose Machine**: Select Red, Blue, Yellow, or Items
4. **Pull**: Choose 1-pull or 10-pull based on your budget
5. **Collect**: Watch the animation and see your results!
6. **Complete**: Collect all 151 Pokémon and 79 items!

### 💡 Pro Tips

- **Yellow Machine** has 2x legendary rates but costs 50% more
- Check the **INFO** button for drop rates and recommendations
- Use the **"Pull Again"** button to quickly repeat pulls
- **Mute** button remembers your preference
- **Reset** button clears everything to start fresh

---

## 🖥️ Play Locally (Desktop)

### Prerequisites
- Python 3.11+
- Pygame 2.6+

### Installation

```bash
# Clone the repository
git clone https://github.com/USERNAME/PokemonBlueGacha.git
cd PokemonBlueGacha

# Install dependencies
pip install pygame

# Run the game
python src/main.py
```

### Run in Browser Locally

```bash
# Install Pygbag
pip install pygbag

# Run locally in browser
pygbag .

# Opens at http://localhost:8000
```

---

## 📁 Project Structure

```
PokemonBlueGacha/
├── src/
│   ├── main.py                 # Entry point
│   ├── config.py               # Game configuration
│   ├── managers/               # Resource, save, state management
│   ├── states/                 # Game states (loading, gacha, inventory)
│   ├── logic/                  # Gacha logic, calculations
│   ├── ui/                     # UI components (buttons, popups, tiles)
│   └── data/                   # Data structures (Pokemon, items, rarities)
├── Assets/
│   ├── Sprites/
│   │   ├── Pokemon/            # 151 Pokemon sprites
│   │   ├── Items/              # 79 item icons
│   │   ├── Types/              # 15 type icons
│   │   └── Main/               # UI sprites
│   ├── Sounds/                 # Sound effects
│   ├── Music/                  # Background music (8 tracks)
│   └── Fonts/                  # Custom fonts
├── data/
│   ├── pokemon_gen1.csv        # Pokemon data (151 entries)
│   ├── items_gen1.csv          # Items data (79 entries)
│   ├── rarity_drop_weights.csv # Rarity weights per machine
│   ├── pokemon_types.csv       # Type definitions
│   └── gacha_machines.csv      # Machine configurations
└── save_data.json              # Player save file (auto-generated)
```

---

## 🛠️ Built With

- **[Python 3.11](https://www.python.org/)** - Core language
- **[Pygame 2.6](https://www.pygame.org/)** - Game framework
- **[Pygbag](https://pygame-web.github.io/)** - Web deployment
- **CSV Data** - Pokémon and item databases
- **Gen 1 Sprites** - Classic Pokémon artwork

---

## 🎲 Gacha System

### Two-Step Weighted Roll

1. **Rarity Roll**: First determine the rarity based on machine weights
2. **Entity Roll**: Then select from available Pokémon/items in that rarity

### Drop Rates (Default)

| Rarity | Red/Blue | Yellow | Items |
|--------|----------|--------|-------|
| Common | 42% | 41% | 60% |
| Uncommon | 36% | 36% | 20% |
| Rare | 15% | 15% | 14% |
| Epic | 6% | 6% | 5% |
| Legendary | 1% | 2% | 1% |

### Version Exclusives

- **Red only**: Oddish, Gloom, Vileplume, Mankey, Primeape, Growlithe, Arcanine, Scyther, Electabuzz
- **Blue only**: Bellsprout, Weepinbell, Victreebel, Meowth, Persian, Vulpix, Ninetales, Pinsir, Magmar
- **Yellow**: All Pokémon available + boosted legendaries

---

## 📊 Statistics & Math

### Expected Pulls Calculator

The game calculates:
- **Pulls to complete each machine** (based on rarest unowned)
- **Optimal strategy** (which machine to prioritize)
- **Expected cost** (total Pokédollars needed)
- **From-scratch pulls** (complete collection starting fresh)

Uses **Coupon Collector Problem** math for accurate estimates!

---

## 🌐 Web Deployment

This game is **100% web-ready**! Deploy to:

- **GitHub Pages** (free, recommended) - See [GITHUB_PAGES_DEPLOYMENT.md](GITHUB_PAGES_DEPLOYMENT.md)
- **Itch.io** (free + game store)
- **Netlify/Vercel** (free tier available)

### Quick Deploy

```bash
# Build for web
pygbag --build .

# Deploy to GitHub Pages
git checkout -b gh-pages
cp -r build/web/* .
git add . && git commit -m "Deploy"
git push -u origin gh-pages
```

See full deployment guide: **[GITHUB_PAGES_DEPLOYMENT.md](GITHUB_PAGES_DEPLOYMENT.md)**

---

## 📱 Mobile Support

✅ **Fully responsive** - works on phones and tablets!  
✅ **Touch controls** - tap = click, swipe = scroll  
✅ **Tested on**: iPhone Safari, Android Chrome, iPad  

---

## 🎵 Audio

### Background Music
- 8 randomized tracks
- Random track on game start
- Random track on unmute
- Click "POKÉDEX" title to shuffle

### Sound Effects
- Button clicks
- Gacha spins
- Pokémon reveal
- Legendary "cha-ching"
- Collection complete celebration

---

## 🎨 Visual Polish

- **Rarity Colors**: White, Green, Blue, Purple, Orange
- **Animated Rays**: Scale and color by rarity
- **Shake Effects**: Individual animation per result
- **NEW! Badges**: Highlight first-time acquisitions
- **Type Icons**: Show dual-type Pokémon correctly
- **Count Labels**: Display owned quantity

---

## 🔧 Configuration

Edit `src/config.py` to customize:

```python
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Machine costs
SINGLE_PULL_COST_RED = 900
SINGLE_PULL_COST_BLUE = 900
SINGLE_PULL_COST_YELLOW = 1350
TEN_PULL_COST_RED = 9000
# ... etc
```

Edit `data/*.csv` to modify:
- Pokémon stats and rarities
- Item values and drop rates
- Gacha machine configurations
- Type colors and icons

---

## 📜 Disclaimer

**This is an unofficial fan-made game.**

Pokémon © 1995-2025 Nintendo / Game Freak / Creatures Inc.

This project is **not affiliated with, endorsed by, or connected to Nintendo, Game Freak, or The Pokémon Company**.

All Pokémon names, sprites, and related media are trademarks and copyrights of their respective owners.

This game is provided **free of charge** for educational and entertainment purposes only.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs
- 💡 Suggest features  
- 🔧 Submit pull requests
- ⭐ Star the repo!

### Development Setup

```bash
# Clone and install
git clone https://github.com/USERNAME/PokemonBlueGacha.git
cd PokemonBlueGacha
pip install pygame pygbag

# Run locally
python src/main.py

# Test web build
pygbag .
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

**TL;DR**: Free to use, modify, and distribute. Keep attribution.

---

## 🙏 Acknowledgments

- **Nintendo/Game Freak** - Original Pokémon games and assets
- **Pygame Community** - Excellent game framework
- **Pygbag Project** - Making web deployment easy
- **PokéAPI & Bulbapedia** - Data sources
- **All contributors and players!**

---

## 📞 Contact

- **GitHub Issues**: [Report bugs](https://github.com/USERNAME/PokemonBlueGacha/issues)
- **Discussions**: [Share ideas](https://github.com/USERNAME/PokemonBlueGacha/discussions)

---

## 🎯 Roadmap

Potential future features:
- [ ] Generation 2 Pokémon (251 total)
- [ ] Shiny variants (rare recolors)
- [ ] Trading system (multiplayer)
- [ ] Daily login bonuses
- [ ] Achievement system
- [ ] Leaderboards
- [ ] Additional gacha machines
- [ ] More item types

**Want to help?** Open an issue or PR!

---

## ⭐ Star History

If you enjoy this game, consider starring the repo! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=USERNAME/PokemonBlueGacha&type=Date)](https://star-history.com/#USERNAME/PokemonBlueGacha&Date)

---

<div align="center">

**Made with ❤️ and Python**

[Play Now](https://USERNAME.github.io/PokemonBlueGacha/) • [Report Bug](https://github.com/USERNAME/PokemonBlueGacha/issues) • [Request Feature](https://github.com/USERNAME/PokemonBlueGacha/issues)

</div>
