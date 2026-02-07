#!/bin/bash
# Installation script for MAC Address Converter (Linux)

set -e

APP_NAME="mac-address-converter"
INSTALL_DIR="$HOME/.local/bin"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_NAME="mac-address-converter.service"
ICON_BASE_DIR="$HOME/.local/share/icons/hicolor"
ICON_DIR="$ICON_BASE_DIR/256x256/apps"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "======================================"
echo "MAC Address Converter - Linux Installer"
echo "======================================"

# Create installation directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$ICON_DIR"
mkdir -p "$DESKTOP_DIR"

# Copy the executable
if [ -f "./dist/$APP_NAME" ]; then
    echo "Installing executable to $INSTALL_DIR..."
    cp "./dist/$APP_NAME" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/$APP_NAME"
    echo "✓ Executable installed"
else
    echo "Error: Executable not found. Please build the application first with: pyinstaller build_config.spec"
    exit 1
fi

# Install icon
if [ -f "./icon.png" ]; then
    echo "Installing icon..."

    # Install the main 256x256 icon
    cp "./icon.png" "$ICON_DIR/$APP_NAME.png"

    # Install additional icon sizes for better desktop environment compatibility
    # These sizes are commonly used by desktop environments
    for size in 48 64 128; do
        size_dir="$ICON_BASE_DIR/${size}x${size}/apps"
        mkdir -p "$size_dir"
        if command -v convert &> /dev/null; then
            convert "./icon.png" -resize ${size}x${size} "$size_dir/$APP_NAME.png" 2>/dev/null || true
        else
            # If ImageMagick is not available, just copy the original
            cp "./icon.png" "$size_dir/$APP_NAME.png"
        fi
    done

    echo "✓ Icon installed (multiple sizes)"

    # Create index.theme file for hicolor theme if it doesn't exist
    HICOLOR_DIR="$ICON_BASE_DIR"
    if [ ! -f "$HICOLOR_DIR/index.theme" ]; then
        echo "Creating hicolor theme index..."
        cat > "$HICOLOR_DIR/index.theme" << 'THEME_EOF'
[Icon Theme]
Name=Hicolor
Comment=Fallback icon theme
Hidden=true
Directories=16x16/apps,22x22/apps,24x24/apps,32x32/apps,48x48/apps,64x64/apps,128x128/apps,256x256/apps,scalable/apps

[16x16/apps]
Size=16
Context=Applications
Type=Threshold

[22x22/apps]
Size=22
Context=Applications
Type=Threshold

[24x24/apps]
Size=24
Context=Applications
Type=Threshold

[32x32/apps]
Size=32
Context=Applications
Type=Threshold

[48x48/apps]
Size=48
Context=Applications
Type=Threshold

[64x64/apps]
Size=64
Context=Applications
Type=Threshold

[128x128/apps]
Size=128
Context=Applications
Type=Threshold

[256x256/apps]
Size=256
Context=Applications
Type=Threshold

[scalable/apps]
Size=48
Context=Applications
Type=Scalable
MinSize=1
MaxSize=512
THEME_EOF
        echo "✓ Hicolor theme index created"
    fi

    # Update icon cache
    if command -v gtk-update-icon-cache &> /dev/null; then
        gtk-update-icon-cache -f -t "$HICOLOR_DIR" 2>/dev/null || true
        echo "✓ Icon cache updated"
    fi
else
    echo "Warning: icon.png not found, skipping icon installation"
fi

# Install desktop file
if [ -f "./$APP_NAME.desktop" ]; then
    echo "Installing desktop file..."
    cp "./$APP_NAME.desktop" "$DESKTOP_DIR/"
    chmod +x "$DESKTOP_DIR/$APP_NAME.desktop"
    echo "✓ Desktop file installed"

    # Update desktop database
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
        echo "✓ Desktop database updated"
    fi
else
    echo "Warning: desktop file not found, skipping desktop integration"
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

echo "✓ Systemd service created"

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
