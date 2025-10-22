# Deployment Script Fixes

## Issues Found During Deployment

During the actual deployment process, we encountered several issues that have now been fixed:

### 1. **File Copying Failed (Windows)**
**Problem:** The Windows `copy` command wasn't working reliably in the batch script context.
```batch
# Old (failed):
copy /Y src\build\web\favicon.png . >nul 2>&1
```

**Solution:** Use PowerShell's `Copy-Item` cmdlet instead:
```batch
# New (works):
powershell -Command "Copy-Item -Path 'src\build\web\favicon.png' -Destination '.' -Force"
```

### 2. **Branch Switching Logic**
**Problem:** The script failed when `gh-pages` branch already existed because it tried to create it anyway.
```batch
# Old:
git checkout gh-pages
if %errorlevel% neq 0 (
    git checkout -b gh-pages
)
```

**Solution:** Properly check for errors and suppress stderr:
```batch
# New:
git checkout gh-pages 2>nul
if %errorlevel% neq 0 (
    echo Creating new gh-pages branch...
    git checkout -b gh-pages
)
```

### 3. **Missing Build Verification**
**Problem:** Script didn't verify that build files were actually created before trying to copy them.

**Solution:** Added build file verification:
```batch
if not exist "src\build\web\index.html" (
    echo ❌ Build files not found!
    pause
    exit /b 1
)
```

### 4. **Commit/Push Logic**
**Problem:** Script would fail if there were no changes to commit.

**Solution:** Check commit exit code before pushing:
```batch
# New:
git commit -m "Deploy: %date% %time%"
if %errorlevel% equ 0 (
    git push origin gh-pages
) else (
    echo ℹ️  No changes to commit
)
```

## What Was Fixed

### deploy.bat (Windows)
✅ **PowerShell Copy-Item** instead of cmd copy  
✅ **Better error suppression** with `2>nul`  
✅ **Build file verification** before copying  
✅ **Improved branch checking** logic  
✅ **Better commit/push flow** that handles "no changes"  
✅ **Clearer error messages** throughout  

### deploy.sh (Linux/Mac)
✅ **Added `set -e`** for automatic error handling  
✅ **Branch existence check** before checkout  
✅ **Build file verification** before copying  
✅ **Individual file copying** instead of wildcard (more predictable)  
✅ **Better commit/push flow** that handles "no changes"  
✅ **Simplified URL output** (removed complex sed commands)  

## Testing Results

Both scripts have been tested and confirmed working:
- ✅ Successfully builds the web version
- ✅ Correctly switches to/creates gh-pages branch
- ✅ Copies all necessary files (favicon.png, index.html, src.apk)
- ✅ Commits and pushes changes
- ✅ Returns to original branch
- ✅ Handles cases where no changes exist

## Usage

### Windows
```batch
.\deploy.bat
```

### Linux/Mac
```bash
chmod +x deploy.sh
./deploy.sh
```

Both scripts will:
1. Build the web version using pygbag
2. Switch to the gh-pages branch (creating it if needed)
3. Copy the built files to the root
4. Commit and push to GitHub
5. Return to your original branch
6. Display the live URL

## Next Deployment

The next time you deploy, simply run the appropriate script and it should work smoothly without any manual intervention!

