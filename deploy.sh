#!/bin/bash
# Quick deployment script for GitHub Pages

set -e  # Exit on error

echo "🚀 Deploying Pokémon Blue Gacha to GitHub Pages..."
echo ""

# Save current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"
echo ""

# Build for web
echo "📦 Building web version..."
pygbag --build src/main.py

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build complete!"
echo ""

# Check if build files exist
if [ ! -f "src/build/web/index.html" ]; then
    echo "❌ Build files not found!"
    exit 1
fi

# Switch to gh-pages
echo "🌿 Switching to gh-pages branch..."
if git rev-parse --verify gh-pages >/dev/null 2>&1; then
    git checkout gh-pages
else
    echo "Creating new gh-pages branch..."
    git checkout -b gh-pages
fi

# Copy build files
echo "📋 Copying build files..."
cp src/build/web/favicon.png . 2>/dev/null || true
cp src/build/web/index.html .
cp src/build/web/src.apk .

if [ ! -f "index.html" ]; then
    echo "❌ Failed to copy files!"
    git checkout $CURRENT_BRANCH
    exit 1
fi

echo "✅ Files copied successfully"
echo ""

# Commit
echo "💾 Committing changes..."
git add favicon.png index.html src.apk
if git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')"; then
    # Push
    echo "🚢 Pushing to GitHub..."
    git push origin gh-pages
else
    echo "ℹ️  No changes to commit"
fi

# Return to original branch
echo "🔙 Returning to $CURRENT_BRANCH branch..."
git checkout $CURRENT_BRANCH

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your game will be live in 2-5 minutes at:"
echo "   https://krool.github.io/PokemonBlueGacha/"
echo ""

