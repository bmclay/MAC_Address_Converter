# Project Structure

## Description
Reference for the MAC Address Converter project layout. Use this when navigating the codebase or deciding where new files should go.

## Directory Layout

```
MAC_Address_Converter/
├── mac_address_converter.py        # Main application (single-file Tkinter app)
├── build_config.spec               # PyInstaller build configuration
├── build.sh                        # Build script for Linux/macOS (bash)
├── build.ps1                       # Build script for Windows (PowerShell)
├── mac-address-converter.desktop   # Linux desktop integration file
├── README.md                       # Project README (displayed on GitHub)
├── LICENSE                         # MIT license
├── .gitignore
│
├── assets/                         # Icons and images
│   ├── icon.png                    # App icon (256x256 PNG, used at runtime)
│   └── icon.ico                    # Windows icon (used by PyInstaller)
│
├── docs/                           # Documentation beyond the README
│   ├── BUILD_INSTRUCTIONS.md       # Detailed build and distribution guide
│   └── DISTRIBUTION.md             # Advanced distribution options (CI/CD, installers)
│
├── scripts/                        # Platform-specific install/uninstall scripts
│   ├── linux/
│   │   ├── install.sh              # Linux installer (systemd service + desktop integration)
│   │   └── uninstall.sh            # Linux uninstaller
│   ├── mac/
│   │   └── install_macos.sh        # macOS installer (LaunchAgent)
│   └── windows/
│       ├── install.ps1             # Windows installer (startup shortcut)
│       └── uninstall.ps1           # Windows uninstaller
│
└── .claude/skills/                 # Claude Code skills (project conventions)
    ├── coding-standards/SKILL.md   # No emojis, Tkinter clipboard, style rules
    ├── command-preference/SKILL.md # Always run commands via tools, don't paste
    └── project-structure/SKILL.md  # This file
```

## Generated Directories (gitignored)

- `dist/` - Build output, organized as `dist/<os>/` (linux, windows, mac)
- `build/` - PyInstaller intermediate files
- `.venv/` - Python virtual environment

## Conventions

### Where files go
- **Source code**: Root directory (single-file app)
- **Icons and images**: `assets/`
- **Documentation**: `docs/` (or root for README.md)
- **Install/uninstall scripts**: `scripts/<os>/`
- **Build output**: `dist/<os>/` (gitignored)
- **Claude skills**: `.claude/skills/<skill-name>/SKILL.md`

### Build workflow
1. Run `./build.sh --pack` (Linux/macOS) or `.\build.ps1 -Pack` (Windows)
2. Build script runs PyInstaller, copies scripts/assets to `dist/<os>/`, creates archive
3. Distribute via GitHub Releases

### Key files
- The app is a single Python file: `mac_address_converter.py`
- PyInstaller bundles `assets/icon.png` into the executable at build time
- Install scripts in `scripts/` are copied into `dist/<os>/` during build
