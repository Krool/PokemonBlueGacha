# 🚀 Deploy to GitHub Pages NOW

## You Already Have a Git Repository - Here's What to Do

---

## ✅ Quick Status Check

- [x] Git repository exists
- [x] Code is async-ready
- [x] Pygbag is installed
- [x] Game works locally

**You're ready to deploy!**

---

## 🎯 Deployment Steps (5 Minutes)

### Step 1: Commit Current Changes (1 minute)

```bash
# Add all the new documentation and code changes
git add .
git commit -m "Add web deployment support and documentation"
git push origin main
```

### Step 2: Build for Web (2 minutes)

```bash
# Build the web version
pygbag --build src/main.py
```

**Note**: Your `main.py` is in the `src/` folder, so we specify `src/main.py`

### Step 3: Deploy to gh-pages (2 minutes)

**Option A: Using the deploy script (Windows)**
```bash
deploy.bat
```

**Option B: Using the deploy script (Mac/Linux)**
```bash
chmod +x deploy.sh
./deploy.sh
```

**Option C: Manual deployment**
```bash
# Create/switch to gh-pages branch
git checkout gh-pages 2>nul || git checkout -b gh-pages

# Copy build files to root
xcopy /E /I /Y build\web\* .

# Remove build folder from gh-pages
rmdir /S /Q build

# Commit and push
git add .
git commit -m "Deploy to GitHub Pages"
git push -u origin gh-pages

# Return to main
git checkout main
```

### Step 4: Enable GitHub Pages (1 minute)

1. Go to your repo: `https://github.com/USERNAME/PokemonBlueGacha`
2. Click **Settings**
3. Click **Pages** (left sidebar)
4. Under **Source**: Select **gh-pages** branch
5. Select **/ (root)** folder
6. Click **Save**

### Step 5: Wait & Access (2-5 minutes)

GitHub will build your site. Refresh the Pages settings to see:

```
✅ Your site is published at https://USERNAME.github.io/PokemonBlueGacha/
```

**Done!** 🎉

---

## 🔄 Future Updates

When you make changes:

```bash
# 1. Make your changes to the code
# 2. Test locally
python src/main.py

# 3. Commit to main
git add .
git commit -m "Your update message"
git push origin main

# 4. Rebuild and redeploy
pygbag --build src/main.py
deploy.bat  # or ./deploy.sh on Mac/Linux
```

---

## 🐛 Troubleshooting

### Pygbag can't find main.py
```bash
# Use explicit path
pygbag --build src/main.py
```

### Deploy script not working
```bash
# Manual deploy
git checkout gh-pages
xcopy /E /I /Y build\web\* .
git add .
git commit -m "Deploy"
git push origin gh-pages
git checkout main
```

### Site shows 404
- Wait 5 minutes (first deploy is slow)
- Check Pages settings: Should say "Your site is published"
- Try incognito mode (clear cache)

---

## 📝 Quick Command Reference

```bash
# Test locally (desktop)
python src/main.py

# Build for web
pygbag --build src/main.py

# Deploy (Windows)
deploy.bat

# Deploy (Mac/Linux)
./deploy.sh

# Check git status
git status
git log --oneline

# Check branches
git branch -a
```

---

## 🎊 That's It!

Your game will be live at:
```
https://USERNAME.github.io/PokemonBlueGacha/
```

Replace `USERNAME` with your GitHub username!

---

## 💡 Pro Tips

1. **Update README.md**: Change `USERNAME` in the play link to your actual GitHub username
2. **Test the live site**: Check all features work in browser
3. **Test on mobile**: Try it on your phone!
4. **Share the link**: Post on social media, Reddit, Discord
5. **Monitor traffic**: Check GitHub Insights tab to see visitors

---

## 🔗 Your Repository Structure

After deployment, you'll have two branches:

**main** - Your source code
```
PokemonBlueGacha/
├── src/
├── Assets/
├── data/
├── README.md
├── etc...
```

**gh-pages** - Your deployed web app
```
PokemonBlueGacha/ (gh-pages branch)
├── index.html
├── pythons.js
├── Assets/
├── data/
├── etc...
```

GitHub Pages serves from the **gh-pages** branch automatically!

---

<div align="center">

# Ready to Deploy?

**Run these commands now:**

```bash
git add .
git commit -m "Add web deployment support"
git push origin main

pygbag --build src/main.py

deploy.bat
```

**Your game will be live in 5 minutes!** 🚀

</div>

