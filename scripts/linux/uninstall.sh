#!/bin/bash
# Uninstall script for MAC Address Converter (Linux)

set -e

APP_NAME="mac-address-converter"
INSTALL_DIR="$HOME/.local/bin"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_NAME="mac-address-converter.service"

echo "======================================"
echo "MAC Address Converter - Linux Uninstaller"
echo "======================================"

# Stop and disable the systemd service
if systemctl --user is-active "$SERVICE_NAME" &> /dev/null; then
    echo "Stopping service..."
    systemctl --user stop "$SERVICE_NAME"
    echo "  Service stopped"
fi

if systemctl --user is-enabled "$SERVICE_NAME" &> /dev/null; then
    echo "Disabling service..."
    systemctl --user disable "$SERVICE_NAME"
    echo "  Service disabled"
fi

# Remove systemd service file
if [ -f "$SERVICE_DIR/$SERVICE_NAME" ]; then
    echo "Removing systemd service file..."
    rm -f "$SERVICE_DIR/$SERVICE_NAME"
    systemctl --user daemon-reload
    echo "  Service file removed"
fi

# Remove executable
if [ -f "$INSTALL_DIR/$APP_NAME" ]; then
    echo "Removing executable..."
    rm -f "$INSTALL_DIR/$APP_NAME"
    echo "  Executable removed"
fi

echo ""
echo "======================================"
echo "Uninstall complete!"
echo "======================================"
echo ""
