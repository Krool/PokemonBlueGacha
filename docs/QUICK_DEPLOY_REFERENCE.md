# ⚡ Quick Deploy Reference Card

## For Users Who Already Have a Git Repo

---

## 🎯 Deploy Right Now (Copy & Paste)

```bash
# 1. Commit current changes
git add .
git commit -m "Add web deployment support and documentation"
git push origin main

# 2. Build for web
pygbag --build src/main.py

# 3. Deploy (choose your OS)

# Windows:
deploy.bat

# Mac/Linux:
chmod +x deploy.sh
./deploy.sh
```

**Then enable Pages**: GitHub repo → Settings → Pages → Source: gh-pages branch → Save

**Your game URL**: `https://YOUR_GITHUB_USERNAME.github.io/PokemonBlueGacha/`

---

## 🔄 Update Deployed Game Later

```bash
# After making code changes:
git add .
git commit -m "Your update message"
git push origin main

# Rebuild and redeploy:
pygbag --build src/main.py
deploy.bat  # or ./deploy.sh
```

---

## 📋 Files Changed This Session

### Code Changes (2 files)
- ✅ `src/main.py` - Added async/await for web support
- ✅ `src/managers/game_data.py` - Reset now includes currency

### Documentation Added (13 files)
- ✅ `README.md` - Main repository README
- ✅ `LICENSE` - MIT license
- ✅ `.gitignore` - Git ignore rules
- ✅ `deploy.bat` - Windows deploy script
- ✅ `deploy.sh` - Linux/Mac deploy script
- ✅ `GITHUB_PAGES_DEPLOYMENT.md` - Full deployment guide
- ✅ `DEPLOYMENT_READY.md` - Deployment checklist
- ✅ `DEPLOY_NOW.md` - Quick deploy (for existing repos)
- ✅ `QUICK_DEPLOY_REFERENCE.md` - This file
- ✅ Plus 4 more support docs

---

## 🎮 What Your Players Will Get

- 🌐 Web URL they can visit (no download!)
- 📱 Works on mobile (touch controls)
- 💾 Saves persist in browser
- 🎵 Background music (8 tracks)
- 🎰 All 4 gacha machines
- 📖 Full Pokédex (151 Pokémon)
- 🎒 Items gacha (79 items)
- 🆓 Completely free to play

---

## ⚠️ Important Notes

### Before Deploying
- ✅ Test game works: `python src/main.py`
- ✅ Update README.md: Change `USERNAME` to your GitHub username
- ✅ Read LICENSE: Understand Pokémon disclaimer

### After Deploying
- ⏳ Wait 5 minutes for first deployment
- 🌐 Test the live URL in browser
- 📱 Test on mobile device
- 🔗 Share the link!

---

## 💰 Cost: $0

GitHub Pages is completely free for public repos!

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "pygbag not found" | `pip install pygbag` |
| "No main.py found" | Use `pygbag --build src/main.py` |
| "Build failed" | Check Python 3.11+, Pygame 2.6+ |
| "Site shows 404" | Wait 5 min, enable Pages in settings |
| "Game won't load" | Clear browser cache, try incognito |

---

## 📞 Need More Help?

- **Full guide**: Read `GITHUB_PAGES_DEPLOYMENT.md`
- **Quick guide**: Read `DEPLOY_NOW.md`
- **All changes**: Read `SESSION_SUMMARY.md`
- **Doc index**: Read `DOCS_INDEX.md`

---

<div align="center">

**Ready? Run these 3 commands:**

```bash
git add . && git commit -m "Deploy" && git push
pygbag --build src/main.py
deploy.bat
```

**🎉 Your game will be live in 5 minutes!**

</div>

