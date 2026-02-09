#!/bin/bash
# Installation script for MAC Address Converter (Linux)

set -e

# Resolve script directory so paths work regardless of where it's run from
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

APP_NAME="mac-address-converter"
INSTALL_DIR="$HOME/.local/bin"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_NAME="mac-address-converter.service"

echo "======================================"
echo "MAC Address Converter - Linux Installer"
echo "======================================"

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Copy the executable (located next to this script in the dist package)
if [ -f "$SCRIPT_DIR/$APP_NAME" ]; then
    echo "Installing executable to $INSTALL_DIR..."
    cp "$SCRIPT_DIR/$APP_NAME" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/$APP_NAME"
    echo "  Executable installed"
else
    echo "Error: Executable not found at $SCRIPT_DIR/$APP_NAME"
    echo "Please build the application first with: ./build.sh"
    exit 1
fi

# Create systemd service directory
mkdir -p "$SERVICE_DIR"

# Create systemd service file
echo "Creating systemd service..."
cat > "$SERVICE_DIR/$SERVICE_NAME" << EOF
[Unit]
Description=MAC Address Converter
After=graphical-session.target

[Service]
Type=simple
ExecStart=$INSTALL_DIR/$APP_NAME
Restart=on-failure
RestartSec=5
Environment="DISPLAY=:0"
Environment="WAYLAND_DISPLAY=wayland-0"
Environment="XDG_RUNTIME_DIR=/run/user/%U"

[Install]
WantedBy=default.target
EOF

echo "  Systemd service created"

# Reload systemd and enable the service
echo "Enabling service to start on login..."
systemctl --user daemon-reload
systemctl --user enable "$SERVICE_NAME"
systemctl --user start "$SERVICE_NAME"

echo ""
echo "======================================"
echo "Installation complete!"
echo "======================================"
echo ""
echo "The MAC Address Converter is now running and will start automatically on login."
echo ""
echo "Useful commands:"
echo "  Stop service:    systemctl --user stop $SERVICE_NAME"
echo "  Start service:   systemctl --user start $SERVICE_NAME"
echo "  Disable service: systemctl --user disable $SERVICE_NAME"
echo "  View logs:       journalctl --user -u $SERVICE_NAME -f"
echo ""
