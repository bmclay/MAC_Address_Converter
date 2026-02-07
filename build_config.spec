# PyInstaller spec file for MAC Address Converter
# Build with: pyinstaller build_config.spec

import sys
from PyInstaller.utils.hooks import collect_all

block_cipher = None

a = Analysis(
    ['mac_address_converter.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.png', '.')],  # Include icon in the build
    hiddenimports=['tkinter'],
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
    name='mac-address-converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # Windows icon
)

# macOS-specific app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='MAC Address Converter.app',
        icon='icon.icns',  # macOS icon (create with: iconutil -c icns icon.iconset)
        bundle_identifier='com.macaddressconverter.app',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': 'True',
        },
    )
