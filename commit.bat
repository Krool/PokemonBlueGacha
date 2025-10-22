@echo off
REM Quick commit script - commits and pushes main branch changes

echo 📝 Committing changes to main branch...
echo.

if "%~1"=="" (
    set COMMIT_MSG=Update code
) else (
    set COMMIT_MSG=%*
)

echo Commit message: %COMMIT_MSG%
echo.

git add -A
git commit -m "%COMMIT_MSG%"

if %errorlevel% equ 0 (
    echo.
    echo 🚢 Pushing to GitHub...
    git push origin main
    
    if %errorlevel% equ 0 (
        echo.
        echo ✅ Changes committed and pushed!
    ) else (
        echo.
        echo ❌ Push failed!
        pause
        exit /b 1
    )
) else (
    echo.
    echo ℹ️ No changes to commit
)

echo.
pause

