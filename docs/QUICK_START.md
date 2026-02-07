# Quick Start Guide

## For Developers: Building Distributable Packages

### 1. Build the Executable

First, ensure you have the dependencies:
```bash
pip install pyinstaller pyperclip
```

Then build for your platform:
```bash
pyinstaller build_config.spec
```

This creates a standalone executable in the `dist/` folder that users can run **without Python installed**.

### 2. Test Locally

Test the executable:
- **Linux**: `./dist/mac-address-converter`
- **Windows**: `dist\mac-address-converter.exe`
- **macOS**: Open `dist/MAC Address Converter.app`

### 3. Create Distribution Package

Create a ZIP file containing:
- The `dist/` folder
- The appropriate installer script (`install.sh`, `install.ps1`, or `install_macos.sh`)
- The uninstaller script (if available)

Example for Linux:
```bash
zip -r mac-address-converter-linux.zip dist/ install.sh uninstall.sh
```

### 4. Share with Users

Upload to GitHub Releases, your website, or share directly.

---

## For End Users: Installing MAC Address Converter

### Linux Installation

1. Extract the downloaded ZIP file
2. Open a terminal in the extracted folder
3. Run:
   ```bash
   ./install.sh
   ```
4. Done! The app will now start automatically when you log in.

### Windows Installation

1. Extract the downloaded ZIP file
2. Right-click `install.ps1` and select "Run with PowerShell"
3. Done! The app will now start automatically when you log in.

### macOS Installation

1. Extract the downloaded ZIP file
2. Open Terminal in the extracted folder
3. Run:
   ```bash
   ./install_macos.sh
   ```
4. Done! The app will now start automatically when you log in.

---

## Using the App

1. Copy any MAC address (e.g., `AA:BB:CC:DD:EE:FF`)
2. The converter window appears automatically
3. Click the format you need
4. The formatted MAC address is now in your clipboard
5. Paste it wherever you need

---

## Uninstalling

### Linux
```bash
./uninstall.sh
```

### Windows
Right-click `uninstall.ps1` and select "Run with PowerShell"

### macOS
Follow the uninstall instructions shown at the end of the installer
