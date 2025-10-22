# 🚀 GitHub Pages Deployment Guide

## Pokémon Blue Gacha - Public Web Deployment

This guide will help you deploy your Pokémon Blue Gacha game to GitHub Pages for **free public hosting**.

---

## 📋 Prerequisites

- [x] ✅ Async conversion complete
- [x] ✅ Pygbag installed (`pip install pygbag`)
- [ ] GitHub account
- [ ] Git installed on your computer

---

## 🎯 Quick Deployment (15 minutes)

### Step 1: Build for Web (2 minutes)

```bash
# Navigate to project root
cd C:\Users\junk7\PokemonBlueGacha

# Build the web version
pygbag --build .
```

This creates `build/web/` with all necessary files.

---

### Step 2: Initialize Git Repository (if not already done)

```bash
# Initialize git (skip if already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - Pokémon Blue Gacha"
```

---

### Step 3: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `PokemonBlueGacha` (or your preferred name)
3. **Public** (required for free GitHub Pages)
4. Don't initialize with README (we have files already)
5. Click **Create repository**

---

### Step 4: Push to GitHub

```bash
# Add your GitHub repo as remote (replace USERNAME)
git remote add origin https://github.com/USERNAME/PokemonBlueGacha.git

# Push main branch
git branch -M main
git push -u origin main
```

---

### Step 5: Deploy to GitHub Pages

**Option A: Using gh-pages branch (Recommended)**

```bash
# Create and switch to gh-pages branch
git checkout -b gh-pages

# Copy web build to root
cp -r build/web/* .

# Remove build folder from gh-pages
rm -rf build

# Commit and push
git add .
git commit -m "Deploy to GitHub Pages"
git push -u origin gh-pages

# Switch back to main
git checkout main
```

**Option B: Using docs folder**

```bash
# Create docs folder and copy build
mkdir docs
cp -r build/web/* docs/

# Commit and push
git add docs
git commit -m "Add GitHub Pages deployment"
git push
```

---

### Step 6: Enable GitHub Pages

1. Go to your repo on GitHub
2. Click **Settings** → **Pages** (left sidebar)
3. **Source**: Deploy from a branch
4. **Branch**: 
   - For Option A: Select `gh-pages` → `/` (root)
   - For Option B: Select `main` → `/docs`
5. Click **Save**

---

### Step 7: Wait and Access (2-5 minutes)

GitHub Pages will build and deploy your site. You'll see:

```
✅ Your site is live at: https://USERNAME.github.io/PokemonBlueGacha/
```

**First deployment takes 2-5 minutes**. Subsequent updates are faster (30 seconds).

---

## 🌐 Your Game is Now Live!

**URL**: `https://USERNAME.github.io/PokemonBlueGacha/`

Share this link with anyone! They can play directly in their browser.

---

## 🔄 Updating Your Game

### When you make changes:

```bash
# Make your code changes
# Test locally: python src/main.py

# Rebuild for web
pygbag --build .

# Switch to gh-pages branch
git checkout gh-pages

# Copy new build
cp -r build/web/* .

# Commit and push
git add .
git commit -m "Update game - [describe changes]"
git push

# Switch back to main
git checkout main
```

**Your site updates in ~30 seconds!**

---

## 🎨 Custom Domain (Optional)

### Using your own domain (e.g., pokemongacha.com):

1. **Buy a domain** (Namecheap, Google Domains, etc.)

2. **Add CNAME file**:
```bash
echo "yourdomain.com" > build/web/CNAME
```

3. **Configure DNS** (at your domain registrar):
```
Type: A
Host: @
Value: 185.199.108.153

Type: A
Host: @
Value: 185.199.109.153

Type: A
Host: @
Value: 185.199.110.153

Type: A
Host: @
Value: 185.199.111.153

Type: CNAME
Host: www
Value: USERNAME.github.io
```

4. **Enable HTTPS** (in GitHub Pages settings)

**Wait 24-48 hours** for DNS propagation.

---

## 📱 Mobile & Desktop Testing

Your game automatically works on:

✅ **Desktop Browsers**:
- Chrome (best performance)
- Firefox
- Safari
- Edge

✅ **Mobile Browsers**:
- iPhone Safari
- Android Chrome
- iPad Safari
- Android tablets

Test on different devices before sharing widely!

---

## 🔒 Privacy & Legal

### Important Considerations:

1. **Public Repository**: 
   - Your code is visible to everyone
   - Anyone can fork/clone your repo

2. **Pokémon Assets**:
   - This is a **fan game** using Pokémon IP
   - Add a disclaimer:
     ```
     This is an unofficial fan-made game. 
     Pokémon © Nintendo/Game Freak.
     Not affiliated with or endorsed by Nintendo.
     ```

3. **No Monetization**:
   - Don't charge for the game
   - Don't include ads
   - Keep it free for legal safety

4. **Educational/Parody**:
   - Can add "Educational purposes" or "Parody" disclaimer
   - Consider making it "Gacha Game Template" with replaceable assets

### Add Disclaimer to Game:

Edit `src/states/loading_state.py` to show disclaimer:
```python
# In render method, add:
disclaimer = "Fan-made game. Pokémon © Nintendo/Game Freak"
disclaimer_surface = self.font_manager.render_text(disclaimer, 12, (150, 150, 150))
self.screen.blit(disclaimer_surface, (10, SCREEN_HEIGHT - 25))
```

---

## 📊 Analytics (Optional)

### Track visitors with Google Analytics:

1. Create GA4 property
2. Get tracking ID
3. Add to `build/web/index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 🐛 Troubleshooting

### Game doesn't load
- **Check browser console** (F12)
- **Clear cache** (Ctrl+Shift+Delete)
- **Try incognito mode**
- **Wait 5 minutes** (first load is slow)

### 404 Error
- **Wait 2-5 minutes** (first deployment)
- **Check branch name** in Pages settings
- **Verify files are in root** of gh-pages branch

### Music doesn't play
- **Click anywhere** first (browser autoplay policy)
- **Check browser console** for errors
- **Test on Chrome** (best audio support)

### Saves don't persist
- **Not in private/incognito** mode
- **Browser storage enabled**
- **Try different browser**

### Slow performance
- **Use Chrome** (fastest WebAssembly)
- **Close other tabs**
- **Try on desktop** vs mobile

---

## 🎯 Deployment Checklist

- [x] ✅ Async conversion complete
- [ ] Build with: `pygbag --build .`
- [ ] Test build locally
- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Create gh-pages branch
- [ ] Copy build files to gh-pages
- [ ] Push gh-pages branch
- [ ] Enable Pages in settings
- [ ] Wait 2-5 minutes
- [ ] Test live site
- [ ] Test on mobile
- [ ] Share URL!

---

## 📈 Expected Performance

| Metric | Value |
|--------|-------|
| Build size | ~20 MB uncompressed |
| Compressed size | ~6-8 MB (gzipped) |
| First load time | 5-10 seconds |
| Subsequent loads | <1 second (cached) |
| FPS (desktop) | 50-60 |
| FPS (mobile) | 40-50 |

---

## 🚀 Your Game URLs

### Main Site
```
https://USERNAME.github.io/PokemonBlueGacha/
```

### Direct Build (if using docs)
```
https://USERNAME.github.io/PokemonBlueGacha/docs/
```

### Repository
```
https://github.com/USERNAME/PokemonBlueGacha
```

---

## 🎊 Success Metrics

Once deployed, you can track:
- **GitHub Stars**: Repo popularity
- **Forks**: People copying your code
- **Traffic**: Views (in Insights tab)
- **Google Analytics**: Detailed visitor stats (if added)

---

## 💡 Pro Tips

1. **README.md**: Add a nice README with:
   - Game description
   - Play link
   - Screenshots
   - Features list

2. **Screenshots**: Take in-game screenshots for README

3. **GIF Demo**: Record gameplay GIF for README

4. **LICENSE**: Add MIT or similar license

5. **Contributing**: If you want contributions, add CONTRIBUTING.md

---

## 📝 Sample README.md for GitHub

```markdown
# 🎮 Pokémon Blue Gacha

A browser-based gacha game featuring all 151 Generation 1 Pokémon!

## 🎯 Play Now

**[▶️ Play Game](https://USERNAME.github.io/PokemonBlueGacha/)**

## ✨ Features

- 🎰 Three Pokémon gacha machines (Red, Blue, Yellow)
- 🎒 Items gacha with 79 Gen 1 items
- 📖 Full Pokédex tracking (151 Pokémon)
- 💾 Persistent save system
- 🎵 8 background music tracks
- 📱 Mobile-friendly (touch controls)
- 🆓 Completely free to play

## 🎮 How to Play

1. Click to add Pokédollars (or use the money button)
2. Open the gacha from your Pokédex
3. Choose a machine (Red, Blue, Yellow, or Items)
4. Pull 1 or 10 at a time
5. Collect all 151 Pokémon!

## 🛠️ Built With

- Python 3.11
- Pygame 2.6
- Pygbag (for web deployment)

## 📜 Disclaimer

This is an unofficial fan-made game. Pokémon © Nintendo/Game Freak.
Not affiliated with or endorsed by Nintendo.

## 🤝 Contributing

Feel free to fork and improve! Pull requests welcome.

## 📄 License

MIT License - see LICENSE file

---

Made with ❤️ by [Your Name]
```

---

## 🎉 You're Ready to Deploy!

**Next command**:
```bash
pygbag --build .
```

Then follow Steps 2-7 above!

Your game will be live and playable by anyone in the world! 🌍

**Share your link with friends and enjoy!** 🎮

