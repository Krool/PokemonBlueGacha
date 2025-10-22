# Quick Scripts Reference

## 📋 Available Scripts

### 1. `commit.bat` - Commit & Push to Main
Quickly commit and push changes to the main branch.

**Usage:**
```batch
# With custom message
.\commit.bat "Fix save system bug"

# With default message "Update code"
.\commit.bat
```

**What it does:**
- ✅ `git add -A` (stages all changes)
- ✅ `git commit -m "your message"`
- ✅ `git push origin main`

---

### 2. `deploy.bat` - Build & Deploy to GitHub Pages
Build the web version and deploy to GitHub Pages.

**Usage:**
```batch
.\deploy.bat
```

**What it does:**
- ✅ `pygbag --build src/main.py` (builds web version)
- ✅ Switches to `gh-pages` branch
- ✅ Copies build files (favicon.png, index.html, src.apk)
- ✅ Commits and pushes to `gh-pages`
- ✅ Returns to original branch

---

### 3. `commit-and-deploy.bat` - All-in-One
Commit changes AND deploy in one command!

**Usage:**
```batch
# With custom message
.\commit-and-deploy.bat "Add localStorage save system"

# With default message "Update and deploy"
.\commit-and-deploy.bat
```

**What it does:**
- ✅ Commits and pushes to `main` branch
- ✅ Builds web version
- ✅ Deploys to `gh-pages` branch
- ✅ **Single confirmation, no tedious clicking!**

---

## 🚀 Common Workflows

### Quick Fix and Deploy
```batch
# Make your code changes, then:
.\commit-and-deploy.bat "Fix audio bug"

# That's it! One command does everything.
```

### Just Commit (No Deploy)
```batch
# When you want to save progress but not deploy:
.\commit.bat "Work in progress"
```

### Just Deploy (Already Committed)
```batch
# If you already committed to main, just deploy:
.\deploy.bat
```

---

## 💡 Tips

### Custom Commit Messages
Always use descriptive messages:
```batch
# Good
.\commit.bat "Fix localStorage persistence issue"
.\commit.bat "Add user interaction detection for web audio"

# Bad
.\commit.bat "fix"
.\commit.bat "update"
```

### Check Status First
```batch
# See what changed before committing
git status

# See what's different
git diff
```

### Verify Deployment
After deploying, check:
1. **GitHub Actions**: https://github.com/Krool/PokemonBlueGacha/actions
2. **Live Site**: https://krool.github.io/PokemonBlueGacha/
3. **Wait 2-5 minutes** for GitHub Pages to update

---

## 🐛 Troubleshooting

### "Build failed!"
- Check that `pygbag` is installed: `pip install pygbag`
- Make sure `src/main.py` exists and has no syntax errors

### "Push failed!"
- Check your internet connection
- Verify GitHub authentication: `git config --list`
- Try: `git pull origin main` first

### "No changes to commit"
- This is normal if you haven't changed any files
- Script will continue to deploy if using `commit-and-deploy.bat`

### Files not copying
- Make sure the build completed successfully
- Check that `src/build/web/` directory exists
- The script now uses individual `copy` commands (more reliable)

---

## 🔧 Advanced: Creating Your Own Scripts

### Template for Custom Script
```batch
@echo off
echo 🚀 My Custom Script
echo.

REM Your commands here
git add specific-file.py
git commit -m "Custom message"
git push origin main

echo ✅ Done!
pause
```

### Make it Executable
Just save as `.bat` file and double-click or run from terminal.

---

## 📝 Script Comparison

| Script | Commits Main | Builds Web | Deploys gh-pages | Confirmations |
|--------|--------------|------------|------------------|---------------|
| `commit.bat` | ✅ | ❌ | ❌ | 1 |
| `deploy.bat` | ❌ | ✅ | ✅ | 1 |
| `commit-and-deploy.bat` | ✅ | ✅ | ✅ | **1** |

**Before improvement**: ~20 confirmations (git add, git commit, git push, build, checkout, copy files, etc.)

**After improvement**: **1 confirmation** for the whole workflow! 🎉

---

## 🎯 Recommended Usage

### Daily Development
```batch
# When actively working
.\commit.bat "Add feature X"
.\commit.bat "Fix bug Y"

# When ready to deploy (end of day/session)
.\deploy.bat
```

### Quick Iterations
```batch
# Make change, test locally
# When ready to push live immediately
.\commit-and-deploy.bat "Fix critical bug"
```

### Safe Approach
```batch
# Commit frequently
.\commit.bat "Save progress"

# Deploy when stable
.\deploy.bat
```

---

## 🔗 Related Documentation
- [Deployment Guide](WEB_DEPLOYMENT_GUIDE.md)
- [GitHub Pages Setup](README_WEB_DEPLOYMENT.md)
- [Development History](DEVELOPMENT_HISTORY.md)


