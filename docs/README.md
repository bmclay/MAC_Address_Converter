# MAC Address Converter

> 🚀 A cross-platform utility that automatically detects copied MAC addresses and provides instant formatting options.

[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-blue)](https://github.com/yourusername/MAC_Address_Converter)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-yellow)](https://www.python.org/)

![MAC Address Converter Screenshot](./mac_address_converter.png)

## ✨ Features

- 🎯 **Automatic Detection** - Monitors your clipboard and detects MAC addresses instantly
- 🔄 **Multiple Formats** - Convert to colons, dashes, dots, or no delimiters
- 🔡 **Case Conversion** - Toggle between uppercase and lowercase
- ⚡ **Zero Friction** - Popup appears only when you copy a MAC address
- 🚀 **Auto-start** - Runs automatically on login as a background service
- 🖥️ **Cross-platform** - Works on Linux, Windows, and macOS
- 📦 **Standalone** - No Python installation required for end users

## 🎬 How It Works

1. Copy a MAC address in any format (e.g., `AA:BB:CC:DD:EE:FF`)
2. The converter window appears automatically
3. Click your desired format
4. The formatted MAC address is now in your clipboard
5. Paste it wherever you need

## 📥 Installation

### For End Users

Your administrator will provide a ZIP file for your platform. Extract it and run the installer:

<table>
<tr>
<td width="33%" align="center">

**🐧 Linux**

Extract, then run:

```bash
chmod +x install.sh
./install.sh
```

</td>
<td width="33%" align="center">

**🪟 Windows**

Extract, then right-click `install.ps1` and select **Run with PowerShell**, or run:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

</td>
<td width="33%" align="center">

**🍎 macOS**

Extract, then run:

```bash
chmod +x install_macos.sh
./install_macos.sh
```

</td>
</tr>
</table>

**That's it!** The app will start automatically and run on every login.

> **📝 Note for Linux users:** You may need to install tkinter first:
>
> - Ubuntu/Debian: `sudo apt install python3-tk`
> - Fedora: `sudo dnf install python3-tkinter`

### Building & Distributing

To create the distribution packages for your users, you must build on each target platform (PyInstaller cannot cross-compile).

1. **Install build dependencies:**

   ```bash
   pip install pyinstaller pyperclip
   ```

2. **Build the executable:**

   ```bash
   pyinstaller build_config.spec
   ```

3. **Create the distribution ZIP:**

   **Windows (PowerShell):**

   ```powershell
   Compress-Archive -Path dist\, install.ps1, uninstall.ps1, docs\QUICK_START.md -DestinationPath mac-address-converter-windows.zip
   ```

   **Linux / macOS:**

   ```bash
   zip -r mac-address-converter-linux.zip dist/ install.sh uninstall.sh docs/QUICK_START.md
   zip -r mac-address-converter-macos.zip dist/ install_macos.sh docs/QUICK_START.md
   ```

4. **Share the ZIP** with your users (email, file share, GitHub Releases, etc.)

See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) and [DISTRIBUTION.md](DISTRIBUTION.md) for more options.

### For Developers

If you want to run from source:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/MAC_Address_Converter.git
   cd MAC_Address_Converter
   ```

2. **Install dependencies:**

   ```bash
   # Linux only: sudo apt install python3-tk (or equivalent)
   # No additional Python packages needed!
   ```

3. **Run directly:**
   ```bash
   python3 mac_address_converter.py
   ```

## 🎯 Usage

Once installed, the MAC Address Converter runs silently in the background. Simply copy a MAC address and the converter window will appear automatically with these options:

| Format            | Example                |
| ----------------- | ---------------------- |
| **Colons**        | `AA:BB:CC:DD:EE:FF`    |
| **Dashes**        | `AA-BB-CC-DD-EE-FF`    |
| **Dots**          | `AABB.CCDD.EEFF`       |
| **No Delimiters** | `AABBCCDDEEFF`         |
| **Convert Case**  | Toggle upper/lowercase |

Click any format to copy it to your clipboard instantly.

## 🛠️ Supported Formats

The converter automatically detects MAC addresses in these formats:

- ✅ `AA:BB:CC:DD:EE:FF` (colons)
- ✅ `AA-BB-CC-DD-EE-FF` (dashes)
- ✅ `AABBCCDDEEFF` (no delimiters)
- ✅ `AABB.CCDD.EEFF` (dot notation)

## 🔧 Management

### Check Status

**Linux:**

```bash
systemctl --user status mac-address-converter.service
```

**Windows:**
Check Task Manager → Background Processes

**macOS:**

```bash
launchctl list | grep macaddressconverter
```

### Stop Service

**Linux:**

```bash
systemctl --user stop mac-address-converter.service
```

**Windows:**
End process from Task Manager

**macOS:**

```bash
launchctl unload ~/Library/LaunchAgents/com.macaddressconverter.app.plist
```

### Uninstall

Run the uninstall script included with your installation:

**Linux/macOS:**

```bash
./uninstall.sh
```

**Windows:**

```powershell
uninstall.ps1
```

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Quick installation guide for users and developers
- **[BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)** - How to build executables for distribution
- **[DISTRIBUTION.md](DISTRIBUTION.md)** - Advanced distribution options (CI/CD, package managers, professional installers)
- **[README_DISTRIBUTION.md](README_DISTRIBUTION.md)** - Complete distribution overview

## 🛣️ Roadmap

- [ ] System tray icon with settings
- [ ] Custom format templates
- [ ] OUI (manufacturer) lookup
- [ ] History of converted addresses
- [ ] Hotkey support
- [ ] Dark mode support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and [Tkinter](https://docs.python.org/3/library/tkinter.html) (including native clipboard handling)
- Packaged with [PyInstaller](https://www.pyinstaller.org/)

## 💡 Use Cases

Perfect for:

- 🔧 Network administrators
- 💻 IT professionals
- 🔐 Security engineers
- 📱 Anyone working with MAC addresses regularly

## 🐛 Troubleshooting

### Linux: "No module named '\_tkinter'"

```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### Windows: Antivirus Warning

The executable may trigger false positives. This is common with PyInstaller builds. You can safely add an exception.

### macOS: "App can't be opened"

Right-click the app and select "Open" instead of double-clicking. This is a Gatekeeper security feature for unsigned apps.

## 📧 Support

Having issues? Please [open an issue](https://github.com/yourusername/MAC_Address_Converter/issues) on GitHub.

---

<div align="center">

**Made with ❤️ for network engineers everywhere**

[Report Bug](https://github.com/yourusername/MAC_Address_Converter/issues) · [Request Feature](https://github.com/yourusername/MAC_Address_Converter/issues)

</div>
