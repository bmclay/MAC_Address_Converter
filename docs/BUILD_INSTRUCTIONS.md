# Build and Distribution Instructions

This guide explains how to build distributable packages for MAC Address Converter on all platforms.

## Prerequisites

Ensure you have Python 3.7+ and the required dependencies:

```bash
pip install pyinstaller pyperclip
```

## Building Executables

### For All Platforms

Build the executable for your current platform:

```bash
pyinstaller build_config.spec
```

This creates:
- **Linux**: `dist/mac-address-converter` (standalone binary)
- **Windows**: `dist/mac-address-converter.exe`
- **macOS**: `dist/MAC Address Converter.app` (app bundle)

### Cross-Platform Notes

- **Linux users** building for Linux: The binary will work on distributions with similar glibc versions
- **Windows users** building for Windows: The .exe will work on Windows 10 and later
- **macOS users** building for macOS: The .app will work on macOS 10.13+ (High Sierra and later)

> **Note**: PyInstaller cannot cross-compile. You must build on each target platform separately.

## Installing on User Machines

### Linux

1. Build the executable on a Linux machine
2. Copy the entire `dist` folder and `install.sh` to the user's machine
3. Run the installer:

```bash
chmod +x install.sh
./install.sh
```

To uninstall:
```bash
chmod +x uninstall.sh
./uninstall.sh
```

### Windows

1. Build the executable on a Windows machine
2. Copy the entire `dist` folder and `install.ps1` to the user's machine
3. Right-click `install.ps1` and select "Run with PowerShell"
   - Or open PowerShell and run:
   ```powershell
   powershell -ExecutionPolicy Bypass -File install.ps1
   ```

To uninstall:
```powershell
powershell -ExecutionPolicy Bypass -File uninstall.ps1
```

### macOS

1. Build the executable on a macOS machine
2. Copy the entire `dist` folder and `install_macos.sh` to the user's machine
3. Run the installer:

```bash
chmod +x install_macos.sh
./install_macos.sh
```

To uninstall, run the commands shown at the end of the installer output.

## Distribution Methods

### Option 1: Simple ZIP Distribution (Recommended for Small Scale)

1. Build on each platform
2. Create platform-specific ZIP files:
   ```
   mac-address-converter-windows.zip
     ├── dist/
     │   └── mac-address-converter.exe
     ├── install.ps1
     └── uninstall.ps1

   mac-address-converter-linux.zip
     ├── dist/
     │   └── mac-address-converter
     ├── install.sh
     └── uninstall.sh

   mac-address-converter-macos.zip
     ├── dist/
     │   └── MAC Address Converter.app/
     └── install_macos.sh
   ```

3. Host on GitHub Releases, your website, or send directly to users

### Option 2: Advanced Installers (For Professional Distribution)

#### Windows - Inno Setup

Create a professional Windows installer:

1. Download [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Create an `.iss` script (installer configuration)
3. Compile to create a single `.exe` installer

#### macOS - Create DMG

Create a drag-and-drop DMG installer:

```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "MAC Address Converter" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "MAC Address Converter.app" 175 120 \
  --hide-extension "MAC Address Converter.app" \
  --app-drop-link 425 120 \
  "MAC-Address-Converter-Installer.dmg" \
  "dist/"
```

#### Linux - AppImage

Create a universal Linux binary:

```bash
# Install appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Create AppDir structure
mkdir -p MACAddressConverter.AppDir/usr/bin
cp dist/mac-address-converter MACAddressConverter.AppDir/usr/bin/
# Add AppRun, desktop file, and icon
# ...then build
./appimagetool-x86_64.AppImage MACAddressConverter.AppDir
```

### Option 3: GitHub Releases with CI/CD

Use GitHub Actions to automatically build for all platforms:

1. Set up GitHub Actions workflows
2. Automatically build on push/release
3. Upload artifacts to GitHub Releases
4. Users download platform-specific packages

## Testing

Before distributing:

1. Test the executable runs correctly
2. Test the installer script works
3. Test auto-start functionality (log out and back in)
4. Test uninstaller removes everything cleanly

## User Installation Summary

For users, the installation is simple:

1. **Download** the appropriate package for their OS
2. **Extract** the ZIP file
3. **Run** the installer script
4. **Done** - the app runs automatically on login

No Python installation or technical knowledge required!

## Support & Troubleshooting

Common issues:

- **Linux**: If tkinter is missing, install with `sudo apt install python3-tk` (Ubuntu/Debian) or `sudo dnf install python3-tkinter` (Fedora)
- **Windows**: Some antivirus software may flag the executable. This is a false positive - you may need to add an exception
- **macOS**: Users may need to allow the app in System Preferences > Security & Privacy if downloaded from the internet
