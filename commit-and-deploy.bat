@echo off
REM All-in-one script: Commit changes, build, and deploy to GitHub Pages

echo 🚀 Commit and Deploy Pipeline
echo ================================
echo.

REM Get commit message
if "%~1"=="" (
    set COMMIT_MSG=Update and deploy
) else (
    set COMMIT_MSG=%*
)

echo Commit message: %COMMIT_MSG%
echo.

REM Step 1: Commit changes to main
echo 📝 Step 1: Committing to main branch...
git add -A
git commit -m "%COMMIT_MSG%"

if %errorlevel% equ 0 (
    echo ✅ Changes committed
    echo.
    echo 🚢 Pushing to main...
    git push origin main
    
    if %errorlevel% neq 0 (
        echo ❌ Push to main failed!
        pause
        exit /b 1
    )
    echo ✅ Pushed to main
) else (
    echo ℹ️ No changes to commit on main
)

echo.
echo ================================
echo.

REM Step 2: Build and deploy
echo 📦 Step 2: Building and deploying to GitHub Pages...
echo.

REM Get current branch
for /f "tokens=*" %%a in ('git branch --show-current') do set CURRENT_BRANCH=%%a

REM Build for web
pygbag --build src/main.py

if %errorlevel% neq 0 (
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo ✅ Build complete
echo.

REM Switch to gh-pages
echo 🌿 Switching to gh-pages branch...
git checkout gh-pages
if %errorlevel% neq 0 (
    echo Creating new gh-pages branch...
    git checkout -b gh-pages
)

REM Copy build files
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

echo ✅ Files copied
echo.

REM Commit and push gh-pages
echo 💾 Committing and pushing to gh-pages...
git add favicon.png index.html src.apk
git commit -m "Deploy: %COMMIT_MSG%" || echo (No changes to deploy)
git push -u origin gh-pages

if %errorlevel% neq 0 (
    echo ❌ Push to gh-pages failed!
    git checkout %CURRENT_BRANCH%
    pause
    exit /b 1
)

REM Return to original branch
echo 🔙 Returning to %CURRENT_BRANCH% branch...
git checkout %CURRENT_BRANCH%

echo.
echo ================================
echo ✅ DEPLOYMENT COMPLETE!
echo ================================
echo.
echo 📍 Changes committed to main branch
echo 🌐 Game deployed to: https://krool.github.io/PokemonBlueGacha/
echo ⏱️ Live in 2-5 minutes
echo.
pause

