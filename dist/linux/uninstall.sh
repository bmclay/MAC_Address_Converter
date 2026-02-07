#!/bin/bash
# Uninstallation script for MAC Address Converter (Linux)

APP_NAME="mac-address-converter"
INSTALL_DIR="$HOME/.local/bin"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_NAME="mac-address-converter.service"

echo "======================================"
echo "MAC Address Converter - Uninstaller"
echo "======================================"
echo ""

# Stop and disable the service
if systemctl --user is-active --quiet "$SERVICE_NAME"; then
    echo "Stopping service..."
    systemctl --user stop "$SERVICE_NAME"
fi

if systemctl --user is-enabled --quiet "$SERVICE_NAME"; then
    echo "Disabling service..."
    systemctl --user disable "$SERVICE_NAME"
fi

# Remove service file
if [ -f "$SERVICE_DIR/$SERVICE_NAME" ]; then
    echo "Removing service file..."
    rm "$SERVICE_DIR/$SERVICE_NAME"
    systemctl --user daemon-reload
fi

# Remove executable
if [ -f "$INSTALL_DIR/$APP_NAME" ]; then
    echo "Removing executable..."
    rm "$INSTALL_DIR/$APP_NAME"
fi

echo ""
echo "✓ Uninstallation complete!"
echo ""
