"""
Build script for creating standalone executables
Run this to create installers for Pokémon Blue Gacha
"""
import os
import sys
import shutil
import subprocess

def build_executable():
    """Build standalone executable using PyInstaller"""
    
    print("=" * 60)
    print("BUILDING POKÉMON BLUE GACHA INSTALLER")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("[OK] PyInstaller found")
    except ImportError:
        print("[!] PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[OK] PyInstaller installed")
    
    # Clean previous builds
    try:
        if os.path.exists("build"):
            shutil.rmtree("build")
            print("[OK] Cleaned build directory")
    except PermissionError:
        print("[WARN] Could not clean build directory (files in use)")
    
    try:
        if os.path.exists("dist"):
            shutil.rmtree("dist")
            print("[OK] Cleaned dist directory")
    except PermissionError:
        print("[WARN] Could not clean dist directory (executable may be running)")
        print("[INFO] Close the .exe file and try again, or PyInstaller will overwrite")
    
    # PyInstaller command for Windows
    if sys.platform == "win32":
        command = [
            "pyinstaller",
            "--name=PokemonBlueGacha",
            "--onefile",
            "--windowed",
            "--icon=appicon.ico",
            "--paths=src",  # Add src to Python path
            "--add-data=src/data;data",
            "--add-data=src/Assets;Assets",
            "--hidden-import=pygame",
            "--hidden-import=csv",
            "--hidden-import=json",
            "--hidden-import=asyncio",
            "src/main.py"
        ]
    else:
        # Unix uses colon instead of semicolon
        command = [
            "pyinstaller",
            "--name=PokemonBlueGacha",
            "--onefile",
            "--windowed",
            "--icon=appicon.ico",
            "--paths=src",  # Add src to Python path
            "--add-data=src/data:data",
            "--add-data=src/Assets:Assets",
            "--hidden-import=pygame",
            "--hidden-import=csv",
            "--hidden-import=json",
            "--hidden-import=asyncio",
            "src/main.py"
        ]
    
    print("\nRunning PyInstaller...")
    print(" ".join(command))
    
    try:
        subprocess.check_call(command)
        print("\n" + "=" * 60)
        print("[OK] BUILD SUCCESSFUL!")
        print("=" * 60)
        print(f"\nExecutable location: dist/")
        if sys.platform == "win32":
            print("Windows executable: dist/PokemonBlueGacha.exe")
        elif sys.platform == "darwin":
            print("macOS executable: dist/PokemonBlueGacha")
        else:
            print("Linux executable: dist/PokemonBlueGacha")
        
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Build failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = build_executable()
    
    if success:
        print("\n" + "=" * 60)
        print("NEXT STEPS:")
        print("=" * 60)
        print("1. Test the executable in the dist/ folder")
        print("2. Distribute as-is or create an installer")
        print("3. Share with users!")
        print("=" * 60)
    else:
        print("\nBuild failed. Check errors above.")
        sys.exit(1)

