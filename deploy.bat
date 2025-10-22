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

REM Check if build files exist
if not exist "src\build\web\index.html" (
    echo ❌ Build files not found!
    pause
    exit /b 1
)

REM Switch to gh-pages
echo 🌿 Switching to gh-pages branch...
git checkout gh-pages 2>nul
if %errorlevel% neq 0 (
    echo Creating new gh-pages branch...
    git checkout -b gh-pages
    if %errorlevel% neq 0 (
        echo ❌ Failed to switch to gh-pages branch!
        pause
        exit /b 1
    )
)

REM Copy build files using PowerShell
echo 📋 Copying build files...
powershell -Command "Copy-Item -Path 'src\build\web\favicon.png' -Destination '.' -Force" 2>nul
powershell -Command "Copy-Item -Path 'src\build\web\index.html' -Destination '.' -Force"
powershell -Command "Copy-Item -Path 'src\build\web\src.apk' -Destination '.' -Force"

if not exist index.html (
    echo ❌ Failed to copy files!
    git checkout %CURRENT_BRANCH%
    pause
    exit /b 1
)

echo ✅ Files copied successfully
echo.

REM Commit and push
echo 💾 Committing changes...
git add favicon.png index.html src.apk
git commit -m "Deploy: %date% %time%"

if %errorlevel% equ 0 (
    echo 🚢 Pushing to GitHub...
    git push origin gh-pages
    
    if %errorlevel% neq 0 (
        echo ❌ Push failed!
        git checkout %CURRENT_BRANCH%
        pause
        exit /b 1
    )
) else (
    echo ℹ️  No changes to commit
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

