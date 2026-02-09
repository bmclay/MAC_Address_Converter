# MAC Address Converter

A cross-platform clipboard utility that automatically detects copied MAC addresses and provides instant formatting options via a toast notification.

[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-blue)](https://github.com/bmclay/MAC_Address_Converter)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-yellow)](https://www.python.org/)

## Features

- **Automatic Detection** -- Monitors the clipboard and detects MAC addresses instantly
- **Multiple Formats** -- Convert to colons, dashes, dots, or no delimiters with one click
- **Case Conversion** -- Toggle between uppercase and lowercase
- **Toast Notification** -- A small popup slides in from the bottom-right corner only when a MAC address is copied
- **Auto-dismiss** -- The toast disappears after 5 seconds of inactivity, or stays open while hovered
- **Auto-start** -- Runs automatically on login as a background service
- **Cross-platform** -- Works on Linux, Windows, and macOS
- **Standalone** -- No Python installation required for end users (PyInstaller builds)
- **No External Dependencies** -- Uses only Python standard library and Tkinter

## How It Works

1. The converter runs silently in the background, polling the clipboard every 500ms
2. When a MAC address is copied, a toast notification slides up from the bottom-right corner
3. Click the desired format button
4. The formatted MAC address is copied to the clipboard
5. The toast dismisses and you can paste wherever needed

## Supported Input Formats

The converter detects MAC addresses in the following formats:

| Format         | Example              |
| -------------- | -------------------- |
| Colons         | `AA:BB:CC:DD:EE:FF`  |
| Dashes         | `AA-BB-CC-DD-EE-FF`  |
| Dots           | `AABB.CCDD.EEFF`     |
| No delimiters  | `AABBCCDDEEFF`       |

Any of these can be converted to any other format, in uppercase or lowercase.

## Installation

### For End Users

Download the release archive for your platform, extract it, and run the installer.

**Linux:**

```bash
chmod +x install.sh
./install.sh
```

The installer copies the binary to `~/.local/bin/`, installs the application icon, creates a `.desktop` file, and sets up a systemd user service for auto-start.

**Windows:**

Right-click `install.ps1` and select **Run with PowerShell**, or run:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

The installer copies the executable to `%LOCALAPPDATA%\MACAddressConverter\` and creates a startup shortcut.

**macOS:**

```bash
chmod +x install_macos.sh
./install_macos.sh
```

The installer copies the `.app` bundle to `~/Applications/` and creates a LaunchAgent for auto-start.

**Note for Linux users:** You may need to install tkinter separately:

- Ubuntu/Debian: `sudo apt install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`
- Arch: `sudo pacman -S tk`

### For Developers

To run from source:

```bash
git clone https://github.com/bmclay/MAC_Address_Converter.git
cd MAC_Address_Converter
python3 mac_address_converter.py
```

No additional Python packages are required beyond the standard library (tkinter must be available).

## Building

PyInstaller cannot cross-compile, so you must build on each target platform. Build scripts handle everything automatically.

**Linux / macOS:**

```bash
pip install pyinstaller
./build.sh          # Build only
./build.sh --pack   # Build and create release archive
```

**Windows (PowerShell):**

```powershell
pip install pyinstaller
.\build.ps1          # Build only
.\build.ps1 -Pack    # Build and create release zip
```

The build scripts run PyInstaller, assemble the distribution package (executable + install/uninstall scripts + assets) in `dist/<os>/`, and optionally create a release archive.

See [docs/BUILD_INSTRUCTIONS.md](docs/BUILD_INSTRUCTIONS.md) for manual build steps and platform-specific notes. See [docs/DISTRIBUTION.md](docs/DISTRIBUTION.md) for advanced distribution options.

## Management

### Check Status

**Linux:**

```bash
systemctl --user status mac-address-converter.service
```

**Windows:**

Check Task Manager under Background Processes.

**macOS:**

```bash
launchctl list | grep macaddressconverter
```

### Stop / Start

**Linux:**

```bash
systemctl --user stop mac-address-converter.service
systemctl --user start mac-address-converter.service
```

**Windows:**

End the process from Task Manager. It will restart on next login.

**macOS:**

```bash
launchctl unload ~/Library/LaunchAgents/com.macaddressconverter.app.plist
launchctl load ~/Library/LaunchAgents/com.macaddressconverter.app.plist
```

### Uninstall

Run the uninstall script included with your installation:

**Linux / macOS:**

```bash
./uninstall.sh
```

**Windows:**

```powershell
powershell -ExecutionPolicy Bypass -File uninstall.ps1
```

## Troubleshooting

### Linux: "No module named '\_tkinter'"

Install tkinter for your distribution:

```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### Windows: Antivirus Warning

The executable may trigger false positives. This is common with PyInstaller builds. You can safely add an exception for the application.

### macOS: "App can't be opened"

Right-click the app and select "Open" instead of double-clicking. This is a Gatekeeper security feature for unsigned apps.

## Project Structure

```
MAC_Address_Converter/
  mac_address_converter.py   # Main application
  build_config.spec          # PyInstaller build configuration
  build.sh                   # Build script (Linux/macOS)
  build.ps1                  # Build script (Windows)
  assets/
    icon.png                 # Application icon (PNG)
    icon.ico                 # Application icon (Windows ICO)
  scripts/
    linux/
      install.sh             # Linux installer
      uninstall.sh           # Linux uninstaller
    windows/
      install.ps1            # Windows installer
      uninstall.ps1          # Windows uninstaller
    mac/
      install_macos.sh       # macOS installer
  docs/
    BUILD_INSTRUCTIONS.md    # Detailed build guide
    DISTRIBUTION.md          # Distribution options
```

## Contributing

Contributions are welcome. Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python and [Tkinter](https://docs.python.org/3/library/tkinter.html) using native clipboard handling
- Packaged with [PyInstaller](https://www.pyinstaller.org/)

## Support

Having issues? Please [open an issue](https://github.com/bmclay/MAC_Address_Converter/issues) on GitHub.
