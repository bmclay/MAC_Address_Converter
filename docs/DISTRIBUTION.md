# Distribution Guide for MAC Address Converter

This document explains how to package and distribute MAC Address Converter to end users across all platforms.

## Overview

This project can be distributed as:
1. **Standalone Executable** - No Python installation required
2. **Auto-start Service** - Runs automatically on user login
3. **Simple Installation** - One-click installer scripts

## Quick Distribution Steps

### 1. Build on Each Platform

You need to build on each target platform (PyInstaller doesn't cross-compile):

**On Linux:**
```bash
python3 -m PyInstaller build_config.spec --clean
zip -r mac-address-converter-linux.zip dist/ install.sh uninstall.sh QUICK_START.md
```

**On Windows:**
```powershell
python -m PyInstaller build_config.spec --clean
Compress-Archive -Path dist\, install.ps1, uninstall.ps1, QUICK_START.md -DestinationPath mac-address-converter-windows.zip
```

**On macOS:**
```bash
python3 -m PyInstaller build_config.spec --clean
zip -r mac-address-converter-macos.zip dist/ install_macos.sh QUICK_START.md
```

### 2. Upload to GitHub Releases

1. Create a new release on GitHub
2. Upload all three ZIP files
3. Add release notes

Example release notes:
```markdown
## MAC Address Converter v1.0.0

A cross-platform utility that automatically detects copied MAC addresses and provides formatting options.

### Features
- Automatic clipboard monitoring
- Multiple format conversions (colons, dashes, dots, no delimiters)
- Case conversion
- Auto-start on login

### Installation

Download the appropriate file for your OS:
- **Linux**: `mac-address-converter-linux.zip`
- **Windows**: `mac-address-converter-windows.zip`
- **macOS**: `mac-address-converter-macos.zip`

Extract and run the installer script. See QUICK_START.md for details.

### Requirements
- **Linux**: tkinter (install with `sudo apt install python3-tk` or `sudo dnf install python3-tkinter`)
- **Windows**: None
- **macOS**: None
```

## Alternative Distribution Methods

### Option 1: Direct Download from Website

Host the ZIP files on your website with download links and installation instructions.

### Option 2: Package Managers

**Linux - Create .deb package:**
```bash
# Install fpm
gem install fpm

# Create .deb
fpm -s dir -t deb \
  -n mac-address-converter \
  -v 1.0.0 \
  --description "Automatic MAC address formatter" \
  --license "MIT" \
  --url "https://github.com/yourusername/MAC_Address_Converter" \
  dist/mac-address-converter=/usr/local/bin/
```

**Linux - Create .rpm package:**
```bash
fpm -s dir -t rpm \
  -n mac-address-converter \
  -v 1.0.0 \
  --description "Automatic MAC address formatter" \
  --license "MIT" \
  dist/mac-address-converter=/usr/local/bin/
```

**Windows - Chocolatey:**
Create a Chocolatey package for distribution through the Chocolatey package manager.

**macOS - Homebrew:**
Create a Homebrew formula for distribution through Homebrew Cask.

### Option 3: Professional Installers

**Windows - Inno Setup:**

Create `installer.iss`:
```inno
[Setup]
AppName=MAC Address Converter
AppVersion=1.0
DefaultDirName={autopf}\MAC Address Converter
DefaultGroupName=MAC Address Converter
OutputDir=output
OutputBaseFilename=mac-address-converter-setup

[Files]
Source: "dist\mac-address-converter.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\MAC Address Converter"; Filename: "{app}\mac-address-converter.exe"
Name: "{userstartup}\MAC Address Converter"; Filename: "{app}\mac-address-converter.exe"

[Run]
Filename: "{app}\mac-address-converter.exe"; Description: "Launch MAC Address Converter"; Flags: nowait postinstall skipifsilent
```

Compile with Inno Setup to create a professional Windows installer.

**macOS - DMG Installer:**

```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "MAC Address Converter" \
  --volicon "icon.icns" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "MAC Address Converter.app" 175 120 \
  --hide-extension "MAC Address Converter.app" \
  --app-drop-link 425 120 \
  "MAC-Address-Converter-Installer.dmg" \
  "dist/"
```

## Automated CI/CD with GitHub Actions

Create `.github/workflows/build.yml`:

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          sudo apt-get install python3-tk
          pip install pyinstaller pyperclip
      - name: Build
        run: pyinstaller build_config.spec --clean
      - name: Package
        run: zip -r mac-address-converter-linux.zip dist/ install.sh uninstall.sh QUICK_START.md
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: linux-build
          path: mac-address-converter-linux.zip

  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install pyinstaller pyperclip
      - name: Build
        run: pyinstaller build_config.spec --clean
      - name: Package
        run: Compress-Archive -Path dist\, install.ps1, uninstall.ps1, QUICK_START.md -DestinationPath mac-address-converter-windows.zip
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: windows-build
          path: mac-address-converter-windows.zip

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install pyinstaller pyperclip
      - name: Build
        run: pyinstaller build_config.spec --clean
      - name: Package
        run: zip -r mac-address-converter-macos.zip dist/ install_macos.sh QUICK_START.md
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: macos-build
          path: mac-address-converter-macos.zip

  release:
    needs: [build-linux, build-windows, build-macos]
    runs-on: ubuntu-latest
    steps:
      - name: Download all artifacts
        uses: actions/download-artifact@v3
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            linux-build/mac-address-converter-linux.zip
            windows-build/mac-address-converter-windows.zip
            macos-build/mac-address-converter-macos.zip
```

This automatically builds and releases when you push a git tag like `v1.0.0`.

## Size Considerations

The executables will be larger than the Python script because they bundle Python and all dependencies:
- **Linux**: ~15-25 MB
- **Windows**: ~20-30 MB
- **macOS**: ~15-25 MB

To reduce size:
- Use UPX compression (enabled in spec file)
- Exclude unnecessary modules
- Remove debug symbols

## Security Considerations

**Code Signing:**

- **Windows**: Sign with a code signing certificate to avoid SmartScreen warnings
- **macOS**: Sign and notarize to avoid Gatekeeper warnings
- **Linux**: Not typically required

**Example Windows signing:**
```bash
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist/mac-address-converter.exe
```

## Testing Before Distribution

Always test on clean machines:

1. **Linux**: Test on Ubuntu, Fedora, and Debian
2. **Windows**: Test on Windows 10 and 11
3. **macOS**: Test on at least two recent versions

Test checklist:
- [ ] Executable runs without errors
- [ ] Clipboard monitoring works
- [ ] GUI appears on MAC address copy
- [ ] All format buttons work
- [ ] Installer creates auto-start entry
- [ ] App starts on login after reboot
- [ ] Uninstaller removes everything cleanly
