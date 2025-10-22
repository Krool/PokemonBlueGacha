#!/bin/bash
# Quick deployment script for GitHub Pages

echo "🚀 Deploying Pokémon Blue Gacha to GitHub Pages..."
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

# Save current branch
CURRENT_BRANCH=$(git branch --show-current)

# Switch to gh-pages
echo "🌿 Switching to gh-pages branch..."
git checkout gh-pages || git checkout -b gh-pages

# Copy build files
echo "📋 Copying build files..."
cp -r build/web/* .

# Clean up
rm -rf build

# Commit
echo "💾 Committing changes..."
git add .
git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')"

# Push
echo "🚢 Pushing to GitHub..."
git push -u origin gh-pages

# Return to original branch
echo "🔙 Returning to $CURRENT_BRANCH branch..."
git checkout $CURRENT_BRANCH

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your game will be live in 2-5 minutes at:"
echo "   https://$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/' | sed 's/\//\.github\.io\//')/"
echo ""
echo "💡 Check deployment status:"
echo "   https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/deployments"

