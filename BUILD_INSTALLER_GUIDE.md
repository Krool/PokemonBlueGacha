# Building Installers for Pokémon Blue Gacha

Complete guide to creating standalone installers for Windows, macOS, and Linux.

---

## 🎯 Quick Start

### All Platforms - PyInstaller Method

```bash
# 1. Install PyInstaller
pip install pyinstaller

# 2. Run the build script
python build_installer.py

# 3. Find executable in dist/ folder
```

---

## 🪟 Windows Installer

### Method 1: PyInstaller Only (Simple)

```bash
# Create standalone .exe
python build_installer.py
```

**Output**: `dist/PokemonBlueGacha.exe` (single file, ~50-100 MB)

**Distribution**:
- Zip the `dist/PokemonBlueGacha.exe` file
- Share the zip file
- Users run the .exe directly (no installation needed)

### Method 2: PyInstaller + Inno Setup (Professional)

**Step 1: Create executable**
```bash
python build_installer.py
```

**Step 2: Download Inno Setup**
- Visit: https://jrsoftware.org/isdl.php
- Download and install Inno Setup
- Free and open source

**Step 3: Compile installer**
1. Open Inno Setup Compiler
2. File → Open → Select `installer_windows.iss`
3. Build → Compile
4. Find installer in `installers/` folder

**Output**: `PokemonBlueGacha_Setup_v1.0.0.exe` (professional installer)

**Features**:
- ✅ Proper installation wizard
- ✅ Start menu shortcuts
- ✅ Desktop icon (optional)
- ✅ Uninstaller included
- ✅ Professional appearance

### Method 3: NSIS (Alternative)

```bash
# Install NSIS
# Download from: https://nsis.sourceforge.io/

# Create NSIS script (installer_windows.nsi)
# Then compile with NSIS
```

---

## 🍎 macOS Installer

### Method 1: PyInstaller .app Bundle

```bash
# Use the spec file for better control
pyinstaller PokemonBlueGacha.spec
```

**Output**: `dist/PokemonBlueGacha.app` (macOS application bundle)

**Distribution**:
- Zip the .app bundle
- Users drag to Applications folder
- Double-click to run

### Method 2: DMG Disk Image (Professional)

**Step 1: Create .app bundle**
```bash
pyinstaller PokemonBlueGacha.spec
```

**Step 2: Create DMG**
```bash
# Install create-dmg
brew install create-dmg

# Create DMG with background image
create-dmg \
  --volname "Pokémon Blue Gacha" \
  --volicon "favicon.png" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "PokemonBlueGacha.app" 200 190 \
  --hide-extension "PokemonBlueGacha.app" \
  --app-drop-link 600 185 \
  "PokemonBlueGacha_v1.0.0.dmg" \
  "dist/PokemonBlueGacha.app"
```

**Output**: `PokemonBlueGacha_v1.0.0.dmg` (professional disk image)

### Method 3: PKG Installer

```bash
# macOS native installer
pkgbuild --root dist/PokemonBlueGacha.app \
         --identifier com.yourname.pokemonbluegacha \
         --version 1.0.0 \
         --install-location /Applications \
         PokemonBlueGacha_v1.0.0.pkg
```

---

## 🐧 Linux Installer

### Method 1: PyInstaller Executable

```bash
python build_installer.py
```

**Output**: `dist/PokemonBlueGacha` (Linux executable)

**Distribution**:
- Create tar.gz: `tar -czf PokemonBlueGacha_v1.0.0.tar.gz dist/PokemonBlueGacha`
- Users extract and run: `./PokemonBlueGacha`

### Method 2: AppImage (Universal Linux)

**Step 1: Install appimagetool**
```bash
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
```

**Step 2: Create AppDir structure**
```bash
mkdir -p PokemonBlueGacha.AppDir/usr/bin
cp dist/PokemonBlueGacha PokemonBlueGacha.AppDir/usr/bin/
cp favicon.png PokemonBlueGacha.AppDir/pokemon-blue-gacha.png

# Create .desktop file
cat > PokemonBlueGacha.AppDir/pokemon-blue-gacha.desktop << EOF
[Desktop Entry]
Name=Pokémon Blue Gacha
Exec=PokemonBlueGacha
Icon=pokemon-blue-gacha
Type=Application
Categories=Game;
EOF

# Create AppRun
cat > PokemonBlueGacha.AppDir/AppRun << EOF
#!/bin/bash
SELF=\$(readlink -f "\$0")
HERE=\${SELF%/*}
exec "\$HERE/usr/bin/PokemonBlueGacha" "\$@"
EOF
chmod +x PokemonBlueGacha.AppDir/AppRun
```

**Step 3: Build AppImage**
```bash
./appimagetool-x86_64.AppImage PokemonBlueGacha.AppDir PokemonBlueGacha_v1.0.0.AppImage
```

**Output**: `PokemonBlueGacha_v1.0.0.AppImage` (universal Linux executable)

### Method 3: DEB Package (Debian/Ubuntu)

```bash
# Create package structure
mkdir -p pokemon-blue-gacha_1.0.0/DEBIAN
mkdir -p pokemon-blue-gacha_1.0.0/usr/local/bin
mkdir -p pokemon-blue-gacha_1.0.0/usr/share/applications
mkdir -p pokemon-blue-gacha_1.0.0/usr/share/pixmaps

# Copy files
cp dist/PokemonBlueGacha pokemon-blue-gacha_1.0.0/usr/local/bin/
cp favicon.png pokemon-blue-gacha_1.0.0/usr/share/pixmaps/pokemon-blue-gacha.png

# Create control file
cat > pokemon-blue-gacha_1.0.0/DEBIAN/control << EOF
Package: pokemon-blue-gacha
Version: 1.0.0
Section: games
Priority: optional
Architecture: amd64
Depends: libsdl2-2.0-0
Maintainer: Your Name <your.email@example.com>
Description: Pokémon Blue Gacha Collection Game
 A gacha-style collection game featuring all 151 Generation 1 Pokémon.
EOF

# Create .desktop file
cat > pokemon-blue-gacha_1.0.0/usr/share/applications/pokemon-blue-gacha.desktop << EOF
[Desktop Entry]
Name=Pokémon Blue Gacha
Exec=/usr/local/bin/PokemonBlueGacha
Icon=pokemon-blue-gacha
Type=Application
Categories=Game;
EOF

# Build package
dpkg-deb --build pokemon-blue-gacha_1.0.0
```

**Output**: `pokemon-blue-gacha_1.0.0.deb`

**Install**: `sudo dpkg -i pokemon-blue-gacha_1.0.0.deb`

---

## 📦 Build Commands Reference

### Simple (All Platforms)

```bash
# Install PyInstaller
pip install pyinstaller

# Build with script
python build_installer.py

# Or manually
pyinstaller --name=PokemonBlueGacha \
            --onefile \
            --windowed \
            --icon=favicon.png \
            --add-data="src/data:data" \
            --add-data="src/Assets:Assets" \
            src/main.py
```

### Advanced (Using .spec file)

```bash
# Edit PokemonBlueGacha.spec as needed
# Then build
pyinstaller PokemonBlueGacha.spec
```

---

## 🎨 Customization

### Change Icon

**Windows**:
- Convert your PNG to .ico format
- Use: https://convertio.co/png-ico/
- Replace `favicon.png` with your .ico file in commands

**macOS**:
- Use .icns format
- Convert PNG to ICNS: `sips -s format icns favicon.png --out icon.icns`

**Linux**:
- Use PNG directly

### Change App Name

Edit in:
- `build_installer.py` → `--name` parameter
- `PokemonBlueGacha.spec` → `name` parameter
- `installer_windows.iss` → `#define MyAppName`

### Reduce File Size

```bash
# Use UPX compression
pip install upx
pyinstaller --name=PokemonBlueGacha \
            --onefile \
            --windowed \
            --upx-dir=/path/to/upx \
            src/main.py
```

---

## 🧪 Testing Your Installer

### Windows
1. Copy `dist/PokemonBlueGacha.exe` to a clean Windows machine
2. Run the executable
3. Verify all assets load correctly
4. Check that saves work

### macOS
1. Copy `PokemonBlueGacha.app` to Applications
2. Right-click → Open (first time only, bypasses Gatekeeper)
3. Test functionality

### Linux
1. Make executable: `chmod +x PokemonBlueGacha`
2. Run: `./PokemonBlueGacha`
3. Test on different distros (Ubuntu, Fedora, Arch)

---

## 📊 Expected File Sizes

| Platform | Method | Size |
|----------|--------|------|
| Windows | .exe (onefile) | 50-100 MB |
| Windows | Inno Setup installer | 50-100 MB |
| macOS | .app bundle | 50-100 MB |
| macOS | .dmg disk image | 50-100 MB |
| Linux | Executable | 50-100 MB |
| Linux | AppImage | 50-100 MB |
| Linux | .deb package | 50-100 MB |

---

## ⚠️ Common Issues

### Issue: "Failed to execute script"
**Solution**: Include all hidden imports in .spec file

### Issue: Assets not found
**Solution**: Verify `--add-data` paths are correct

### Issue: Antivirus flags executable
**Solution**: 
- Code sign your executable
- Or whitelist in antivirus
- Or build with `--debug` to see what's happening

### Issue: Large file size
**Solution**: 
- Use `--onefile` instead of `--onedir`
- Enable UPX compression
- Exclude unnecessary modules

---

## 🚀 Distribution Platforms

### Option 1: GitHub Releases
```bash
# Create a release on GitHub
# Upload your installers as assets
# Users can download directly
```

### Option 2: Itch.io
- Upload desktop builds alongside web build
- Support Windows, macOS, Linux
- Built-in download manager

### Option 3: Self-Hosting
- Host installers on your own server
- Link from your website
- Full control over distribution

---

## 📜 Code Signing (Optional but Recommended)

### Windows
```bash
# Requires a code signing certificate
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist/PokemonBlueGacha.exe
```

### macOS
```bash
# Requires Apple Developer account ($99/year)
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/PokemonBlueGacha.app
```

### Linux
- Not typically required
- Can use GPG signatures for package verification

---

## ✅ Checklist

Before distributing:
- [ ] Test executable on clean machine
- [ ] Verify all assets load
- [ ] Check save/load functionality
- [ ] Test audio playback
- [ ] Include README in installer
- [ ] Include LICENSE file
- [ ] Test on multiple OS versions
- [ ] Scan for viruses (VirusTotal.com)
- [ ] Create release notes
- [ ] Update version numbers

---

## 🎉 You're Ready!

Choose your method:
- **Quick & Easy**: PyInstaller → Single executable
- **Professional**: PyInstaller + Inno Setup (Windows) or DMG (macOS)
- **Universal**: AppImage (Linux)

**Recommended Distribution**:
1. Build installers for all platforms
2. Upload to GitHub Releases
3. Also deploy web version (reaches everyone)
4. Provide both options to users

---

For questions or issues, open an issue on GitHub!

