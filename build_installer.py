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
        print("✓ PyInstaller found")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")
    
    # Clean previous builds
    if os.path.exists("build"):
        shutil.rmtree("build")
        print("✓ Cleaned build directory")
    
    if os.path.exists("dist"):
        shutil.rmtree("dist")
        print("✓ Cleaned dist directory")
    
    # PyInstaller command
    command = [
        "pyinstaller",
        "--name=PokemonBlueGacha",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (GUI only)
        "--icon=favicon.png",  # App icon
        
        # Include data files
        "--add-data=src/data;data",
        "--add-data=src/Assets;Assets",
        
        # Hidden imports (if needed)
        "--hidden-import=pygame",
        "--hidden-import=csv",
        "--hidden-import=json",
        
        # Entry point
        "src/main.py"
    ]
    
    # Adjust add-data syntax for Windows
    if sys.platform == "win32":
        command = [
            "pyinstaller",
            "--name=PokemonBlueGacha",
            "--onefile",
            "--windowed",
            "--icon=favicon.png",
            "--add-data=src/data;data",
            "--add-data=src/Assets;Assets",
            "--hidden-import=pygame",
            "--hidden-import=csv",
            "--hidden-import=json",
            "src/main.py"
        ]
    else:
        # Unix uses colon instead of semicolon
        command = [
            "pyinstaller",
            "--name=PokemonBlueGacha",
            "--onefile",
            "--windowed",
            "--icon=favicon.png",
            "--add-data=src/data:data",
            "--add-data=src/Assets:Assets",
            "--hidden-import=pygame",
            "--hidden-import=csv",
            "--hidden-import=json",
            "src/main.py"
        ]
    
    print("\nRunning PyInstaller...")
    print(" ".join(command))
    
    try:
        subprocess.check_call(command)
        print("\n" + "=" * 60)
        print("✓ BUILD SUCCESSFUL!")
        print("=" * 60)
        print(f"\nExecutable location: dist/PokemonBlueGacha")
        if sys.platform == "win32":
            print("Windows executable: dist/PokemonBlueGacha.exe")
        elif sys.platform == "darwin":
            print("macOS executable: dist/PokemonBlueGacha")
        else:
            print("Linux executable: dist/PokemonBlueGacha")
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = build_executable()
    
    if success:
        print("\n" + "=" * 60)
        print("NEXT STEPS:")
        print("=" * 60)
        print("1. Test the executable in the dist/ folder")
        print("2. Create an installer using Inno Setup (Windows)")
        print("3. Or distribute the dist/ folder as a ZIP file")
        print("=" * 60)
    else:
        print("\nBuild failed. Check errors above.")
        sys.exit(1)

