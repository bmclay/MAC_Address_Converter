# MAC Address Converter - Linux Distribution

A background service that monitors your clipboard for MAC addresses and provides a convenient conversion interface.

## Features
- Automatically detects MAC addresses when copied
- Converts between multiple formats (colons, dashes, dots, no delimiters)
- Case conversion
- Runs as a background service on startup
- Modern dark UI theme
- Custom taskbar icon

## System Requirements
- Linux (tested on Fedora, Ubuntu, Debian)
- X11 or Wayland display server
- Python 3.x with Tkinter (for source install only - not needed for pre-built binary)

### For Fedora/RHEL:
```bash
sudo dnf install python3-tkinter
```

### For Ubuntu/Debian:
```bash
sudo apt install python3-tk
```

## Installation

### Quick Install
1. Extract the archive
2. Open a terminal in this directory
3. Run the installer:
```bash
./install.sh
```

The application will:
- Install to `~/.local/bin/mac-address-converter`
- Create a systemd user service
- Set up to start automatically on login
- Install desktop integration files and icon

### What Gets Installed
- **Executable**: `~/.local/bin/mac-address-converter`
- **Desktop File**: `~/.local/share/applications/mac-address-converter.desktop`
- **Icons**: `~/.local/share/icons/hicolor/*/apps/mac-address-converter.png`
- **Service**: `~/.config/systemd/user/mac-address-converter.service`

## Usage

Once installed, the service runs automatically in the background. Simply copy any MAC address (in any format) and the converter window will appear automatically.

### Supported Formats
- **Colons**: `AA:BB:CC:DD:EE:FF`
- **Dashes**: `AA-BB-CC-DD-EE-FF`
- **Dots**: `AABB.CCDD.EEFF`
- **No delimiters**: `AABBCCDDEEFF`

Click any format button to convert and copy it to your clipboard.

## Service Management

### Check Status
```bash
systemctl --user status mac-address-converter.service
```

### Stop Service
```bash
systemctl --user stop mac-address-converter.service
```

### Start Service
```bash
systemctl --user start mac-address-converter.service
```

### Restart Service
```bash
systemctl --user restart mac-address-converter.service
```

### View Logs
```bash
journalctl --user -u mac-address-converter.service -f
```

## Uninstallation

Run the uninstall script:
```bash
./uninstall.sh
```

This will:
- Stop and disable the service
- Remove all installed files
- Clean up systemd configuration

## Troubleshooting

### Icon not showing in taskbar
The icon should display correctly on GNOME/KDE/XFCE. If it doesn't:
1. Restart the service: `systemctl --user restart mac-address-converter.service`
2. Log out and log back in
3. Update icon cache: `gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor/`

### Window not appearing
1. Check if the service is running: `systemctl --user status mac-address-converter.service`
2. Check the logs: `journalctl --user -u mac-address-converter.service`
3. Ensure you copied a valid MAC address format

### Clipboard not being monitored
Make sure you have xclip or xsel installed:
```bash
# Fedora
sudo dnf install xclip

# Ubuntu/Debian
sudo apt install xclip
```

## Support

For issues, please visit: https://github.com/bmclay/MAC_Address_Converter/issues

## License

See LICENSE file in the project repository.
