@echo off
REM Quick deployment script for GitHub Pages (Windows)

echo 🚀 Deploying Pokémon Blue Gacha to GitHub Pages...
echo.

REM Get current branch
for /f "tokens=*" %%a in ('git branch --show-current') do set CURRENT_BRANCH=%%a
echo Current branch: %CURRENT_BRANCH%
echo.

REM Build for web
echo 📦 Building web version...
pygbag --build src/main.py

if %errorlevel% neq 0 (
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo ✅ Build complete!
echo.

REM Switch to gh-pages
echo 🌿 Switching to gh-pages branch...
git checkout gh-pages
if %errorlevel% neq 0 (
    echo Creating new gh-pages branch...
    git checkout -b gh-pages
)

REM Copy build files (using copy command for individual files)
echo 📋 Copying build files...
copy /Y src\build\web\favicon.png . >nul 2>&1
copy /Y src\build\web\index.html . >nul 2>&1
copy /Y src\build\web\src.apk . >nul 2>&1

if not exist index.html (
    echo ❌ Failed to copy files!
    git checkout %CURRENT_BRANCH%
    pause
    exit /b 1
)

echo ✅ Files copied successfully
echo.

REM Commit and push
echo 💾 Committing and pushing changes...
git add favicon.png index.html src.apk
git commit -m "Deploy: %date% %time%" || echo (No changes to commit)
git push -u origin gh-pages

if %errorlevel% neq 0 (
    echo ❌ Push failed!
    git checkout %CURRENT_BRANCH%
    pause
    exit /b 1
)

REM Return to original branch
echo 🔙 Returning to %CURRENT_BRANCH% branch...
git checkout %CURRENT_BRANCH%

echo.
echo ✅ Deployment complete!
echo 🌐 Your game will be live in 2-5 minutes at:
echo    https://krool.github.io/PokemonBlueGacha/
echo.
pause

