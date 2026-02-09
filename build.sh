#!/bin/bash
# Build script for MAC Address Converter
# Builds the PyInstaller binary and assembles the dist package for the current OS.
#
# Usage:
#   ./build.sh          # Build for current OS
#   ./build.sh --pack   # Build and create release archive

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST_DIR="$PROJECT_DIR/dist"
BUILD_DIR="$PROJECT_DIR/build"

PACK=false
if [ "$1" = "--pack" ]; then
    PACK=true
fi

detect_os() {
    case "$(uname -s)" in
        Linux*)  echo "linux" ;;
        Darwin*) echo "mac" ;;
        MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
        *)       echo "unknown" ;;
    esac
}

OS="$(detect_os)"
echo "Building for: $OS"

# Clean previous build artifacts
rm -rf "$BUILD_DIR"
rm -rf "$DIST_DIR/$OS"
mkdir -p "$DIST_DIR/$OS"

# Run PyInstaller
echo "Running PyInstaller..."
pyinstaller "$PROJECT_DIR/build_config.spec" --distpath "$DIST_DIR/$OS" --workpath "$BUILD_DIR" --noconfirm

# The spec produces a single file named 'mac-address-converter' in the dist dir.
# PyInstaller with onefile mode puts it directly in distpath.

# Assemble the distribution package
echo "Assembling distribution package..."

case "$OS" in
    linux)
        cp "$PROJECT_DIR/scripts/linux/install.sh" "$DIST_DIR/$OS/"
        cp "$PROJECT_DIR/scripts/linux/uninstall.sh" "$DIST_DIR/$OS/"
        chmod +x "$DIST_DIR/$OS/install.sh" "$DIST_DIR/$OS/uninstall.sh"
        chmod +x "$DIST_DIR/$OS/mac-address-converter"

        if [ "$PACK" = true ]; then
            echo "Creating release archive..."
            tar -czf "$DIST_DIR/mac-address-converter-linux.tar.gz" -C "$DIST_DIR" linux/
            echo "Archive: $DIST_DIR/mac-address-converter-linux.tar.gz"
        fi
        ;;
    windows)
        cp "$PROJECT_DIR/scripts/windows/install.ps1" "$DIST_DIR/$OS/"
        cp "$PROJECT_DIR/scripts/windows/uninstall.ps1" "$DIST_DIR/$OS/"

        if [ "$PACK" = true ]; then
            echo "Creating release archive..."
            (cd "$DIST_DIR" && zip -r mac-address-converter-windows.zip windows/)
            echo "Archive: $DIST_DIR/mac-address-converter-windows.zip"
        fi
        ;;
    mac)
        cp "$PROJECT_DIR/scripts/mac/install_macos.sh" "$DIST_DIR/$OS/"
        cp "$PROJECT_DIR/scripts/mac/uninstall_macos.sh" "$DIST_DIR/$OS/"
        chmod +x "$DIST_DIR/$OS/install_macos.sh" "$DIST_DIR/$OS/uninstall_macos.sh"

        if [ "$PACK" = true ]; then
            echo "Creating release archive..."
            tar -czf "$DIST_DIR/mac-address-converter-macos.tar.gz" -C "$DIST_DIR" mac/
            echo "Archive: $DIST_DIR/mac-address-converter-macos.tar.gz"
        fi
        ;;
    *)
        echo "Error: Unsupported OS"
        exit 1
        ;;
esac

echo ""
echo "Build complete! Output: $DIST_DIR/$OS/"
ls -la "$DIST_DIR/$OS/"
