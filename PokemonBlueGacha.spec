# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Pokémon Blue Gacha
This provides more control over the build process
"""

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/data', 'data'),
        ('src/Assets', 'Assets'),
    ],
    hiddenimports=[
        'pygame',
        'csv',
        'json',
        'random',
        'asyncio',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PokemonBlueGacha',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI only)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='favicon.png',  # App icon
)

# For macOS: Create .app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='PokemonBlueGacha.app',
        icon='favicon.png',
        bundle_identifier='com.yourname.pokemonbluegacha',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': 'True',
            'CFBundleName': 'Pokémon Blue Gacha',
            'CFBundleDisplayName': 'Pokémon Blue Gacha',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
        },
    )

