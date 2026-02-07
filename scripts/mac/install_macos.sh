#!/bin/bash
# Installation script for MAC Address Converter (macOS)

set -e

APP_NAME="MAC Address Converter.app"
INSTALL_DIR="$HOME/Applications"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_NAME="com.macaddressconverter.app.plist"

echo "======================================"
echo "MAC Address Converter - macOS Installer"
echo "======================================"

# Create installation directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Copy the app bundle
if [ -d "./dist/$APP_NAME" ]; then
    echo "Installing application to $INSTALL_DIR..."
    # Remove old version if exists
    rm -rf "$INSTALL_DIR/$APP_NAME"
    cp -R "./dist/$APP_NAME" "$INSTALL_DIR/"
    echo "✓ Application installed"
else
    echo "Error: Application bundle not found. Please build the application first with: pyinstaller build_config.spec"
    exit 1
fi

# Get the executable path within the app bundle
EXEC_PATH="$INSTALL_DIR/$APP_NAME/Contents/MacOS/mac-address-converter"

# Create launch agent directory
mkdir -p "$LAUNCH_AGENTS_DIR"

# Create launch agent plist
echo "Creating launch agent..."
cat > "$LAUNCH_AGENTS_DIR/$PLIST_NAME" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.macaddressconverter.app</string>
    <key>ProgramArguments</key>
    <array>
        <string>$EXEC_PATH</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>$HOME/Library/Logs/mac-address-converter.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/Library/Logs/mac-address-converter-error.log</string>
</dict>
</plist>
EOF

echo "✓ Launch agent created"

# Load the launch agent
echo "Loading launch agent..."
launchctl unload "$LAUNCH_AGENTS_DIR/$PLIST_NAME" 2>/dev/null || true
launchctl load "$LAUNCH_AGENTS_DIR/$PLIST_NAME"
echo "✓ Launch agent loaded"

echo ""
echo "======================================"
echo "Installation complete!"
echo "======================================"
echo ""
echo "The MAC Address Converter is now running and will start automatically on login."
echo ""
echo "Useful commands:"
echo "  Stop:     launchctl unload $LAUNCH_AGENTS_DIR/$PLIST_NAME"
echo "  Start:    launchctl load $LAUNCH_AGENTS_DIR/$PLIST_NAME"
echo "  Logs:     tail -f ~/Library/Logs/mac-address-converter.log"
echo ""
echo "To uninstall:"
echo "  1. launchctl unload $LAUNCH_AGENTS_DIR/$PLIST_NAME"
echo "  2. rm $LAUNCH_AGENTS_DIR/$PLIST_NAME"
echo "  3. rm -rf '$INSTALL_DIR/$APP_NAME'"
echo ""
