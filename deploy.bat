@echo off
REM Quick deployment script for GitHub Pages (Windows)

echo 🚀 Deploying Pokémon Blue Gacha to GitHub Pages...
echo.

REM Build for web
echo 📦 Building web version...
pygbag --build src/main.py

if %errorlevel% neq 0 (
    echo ❌ Build failed!
    exit /b 1
)

echo ✅ Build complete!
echo.

REM Get current branch
for /f "tokens=*" %%a in ('git branch --show-current') do set CURRENT_BRANCH=%%a

REM Switch to gh-pages
echo 🌿 Switching to gh-pages branch...
git checkout gh-pages
if %errorlevel% neq 0 (
    git checkout -b gh-pages
)

REM Copy build files
echo 📋 Copying build files...
xcopy /E /I /Y src\build\web\* .

REM Clean up
rmdir /S /Q src\build

REM Commit
echo 💾 Committing changes...
git add .
git commit -m "Deploy: %date% %time%"

REM Push
echo 🚢 Pushing to GitHub...
git push -u origin gh-pages

REM Return to original branch
echo 🔙 Returning to %CURRENT_BRANCH% branch...
git checkout %CURRENT_BRANCH%

echo.
echo ✅ Deployment complete!
echo 🌐 Your game will be live in 2-5 minutes!
echo.
echo 💡 Check your GitHub repository Settings → Pages for the URL
pause

