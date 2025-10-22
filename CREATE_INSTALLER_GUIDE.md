# How to Create a Windows Installer

## Quick Steps (5 minutes)

### Step 1: Download Inno Setup
1. Visit: https://jrsoftware.org/isdl.php
2. Download **Inno Setup 6** (free, ~5 MB)
3. Install with default options

### Step 2: Edit the Script (Optional)
Open `installer_windows.iss` and update:
- Line 6: Change `"Your Name"` to your actual name
- Line 7: Replace `USERNAME` with your GitHub username

### Step 3: Create the Installer
1. Open **Inno Setup Compiler**
2. File → Open → Select `installer_windows.iss`
3. Build → Compile (or press Ctrl+F9)
4. Wait 10-20 seconds...

### Step 4: Find Your Installer
Your installer will be in:
```
installers/PokemonBlueGacha_Setup_v1.0.0.exe
```

File size: ~62 MB (same as the .exe, plus installer overhead)

## Distribution

### Share the Installer
Send people: `PokemonBlueGacha_Setup_v1.0.0.exe`

They will get:
- ✅ Professional installation wizard
- ✅ Start Menu shortcut
- ✅ Optional desktop icon
- ✅ Proper uninstaller
- ✅ README and LICENSE included

### Or Share Just the EXE
Alternatively, you can share just:
```
dist/PokemonBlueGacha.exe
```

This is simpler but less professional:
- ✅ No installation needed (just run it)
- ❌ No Start Menu entry
- ❌ No desktop shortcut
- ❌ No uninstaller

## What the Installer Does

1. **Welcome Screen** - Greets the user
2. **License Agreement** - Shows your LICENSE file
3. **Choose Location** - User picks install folder (default: C:\Program Files\PokemonBlueGacha)
4. **Select Components** - Option to create desktop icon
5. **Install** - Copies the .exe file
6. **Finish** - Option to launch game immediately

## Installer Features

### For Users
- **Start Menu**: "Pokémon Blue Gacha" shortcut
- **Uninstall**: Clean removal via Windows Settings
- **Desktop Icon**: Optional shortcut
- **README Access**: Easy access to documentation

### For You
- **Professional**: Proper Windows installer
- **Safe**: Uses standard Windows installer framework
- **Signed**: Can add code signing later (optional, costs money)
- **Updates**: Easy to create new versions

## Advanced Options

### Code Signing (Optional, $100-300/year)
Make Windows trust your installer:
1. Buy a code signing certificate
2. Sign the installer with `signtool`
3. Users won't see "Unknown Publisher" warning

### Custom Graphics (Optional)
Add custom wizard images:
```ini
WizardImageFile=wizard_image.bmp    ; 164x314 pixels
WizardSmallImageFile=wizard_small.bmp  ; 55x55 pixels
```

### Multi-Language (Optional)
Add more languages:
```ini
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
```

## Testing Checklist

Before distributing:
- [ ] Install on a clean Windows PC
- [ ] Verify game launches from Start Menu
- [ ] Test desktop shortcut (if created)
- [ ] Play the game (pull some Pokémon/items)
- [ ] Exit and relaunch (test save persistence)
- [ ] Uninstall cleanly
- [ ] Check that save files remain (in user folder)

## Distribution Platforms

### Option 1: Direct Download
- Upload installer to your website
- Share via Google Drive, Dropbox, etc.
- Send directly to friends

### Option 2: GitHub Releases
```bash
# Create a release on GitHub
1. Go to your repo → Releases → Create Release
2. Tag: v1.0.0
3. Title: "Pokémon Blue Gacha v1.0.0"
4. Upload: PokemonBlueGacha_Setup_v1.0.0.exe
5. Publish
```

### Option 3: Itch.io
- Upload installer as "Windows" build
- Set price (free or paid)
- Itch.io handles downloads and updates

## File Sizes

| File | Size | Description |
|------|------|-------------|
| `PokemonBlueGacha.exe` | ~62 MB | Standalone executable |
| `PokemonBlueGacha_Setup_v1.0.0.exe` | ~63 MB | Installer with wizard |

## Common Issues

### "Windows protected your PC"
- **Why**: Unsigned installer (normal for free apps)
- **Solution**: Click "More info" → "Run anyway"
- **To Fix**: Buy code signing certificate ($$$)

### Antivirus False Positive
- **Why**: New executable, not many downloads yet
- **Solution**: Submit to VirusTotal, report false positive
- **Prevention**: Code signing helps

### Installation Fails
- **Why**: Permissions or disk space
- **Solution**: Run as Administrator, check disk space
- **Prevention**: Use `PrivilegesRequired=lowest` (already set)

## Next Steps

1. **Create installer** (follow steps above)
2. **Test on clean PC** (or VM)
3. **Upload to GitHub Releases**
4. **Share with friends!**

## Support

If users have issues:
- Point them to: https://github.com/USERNAME/PokemonBlueGacha/issues
- Check antivirus settings
- Verify Windows version (Windows 10/11 required)
- Try standalone .exe instead

---

**You're ready!** Create your installer and share your game! 🎮✨

