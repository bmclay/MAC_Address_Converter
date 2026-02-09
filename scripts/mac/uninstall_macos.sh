#!/bin/bash
# Uninstall script for MAC Address Converter (macOS)

set -e

APP_NAME="MAC Address Converter.app"
INSTALL_DIR="$HOME/Applications"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_NAME="com.macaddressconverter.app.plist"

echo "======================================"
echo "MAC Address Converter - macOS Uninstaller"
echo "======================================"

# Unload the launch agent
if [ -f "$LAUNCH_AGENTS_DIR/$PLIST_NAME" ]; then
    echo "Unloading launch agent..."
    launchctl unload "$LAUNCH_AGENTS_DIR/$PLIST_NAME" 2>/dev/null || true
    echo "  Launch agent unloaded"

    echo "Removing launch agent plist..."
    rm -f "$LAUNCH_AGENTS_DIR/$PLIST_NAME"
    echo "  Launch agent plist removed"
fi

# Remove the application
if [ -d "$INSTALL_DIR/$APP_NAME" ]; then
    echo "Removing application..."
    rm -rf "$INSTALL_DIR/$APP_NAME"
    echo "  Application removed"
fi

# Remove standalone binary if present
if [ -f "$INSTALL_DIR/mac-address-converter" ]; then
    echo "Removing executable..."
    rm -f "$INSTALL_DIR/mac-address-converter"
    echo "  Executable removed"
fi

# Remove log files
echo "Removing log files..."
rm -f "$HOME/Library/Logs/mac-address-converter.log"
rm -f "$HOME/Library/Logs/mac-address-converter-error.log"
echo "  Log files removed"

echo ""
echo "======================================"
echo "Uninstall complete!"
echo "======================================"
echo ""
