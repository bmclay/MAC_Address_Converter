# Installation script for MAC Address Converter (Windows)
# Run with: powershell -ExecutionPolicy Bypass -File install.ps1

$ErrorActionPreference = "Stop"

$AppName = "mac-address-converter.exe"
$InstallDir = "$env:LOCALAPPDATA\MACAddressConverter"
$StartupDir = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$ShortcutPath = "$StartupDir\MAC Address Converter.lnk"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "MAC Address Converter - Windows Installer" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Create installation directory
Write-Host "Creating installation directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

# Copy the executable
if (Test-Path ".\dist\$AppName") {
    Write-Host "Installing executable to $InstallDir..." -ForegroundColor Yellow
    Copy-Item ".\dist\$AppName" -Destination "$InstallDir\" -Force
    Write-Host "✓ Executable installed" -ForegroundColor Green
} else {
    Write-Host "Error: Executable not found. Please build the application first with: pyinstaller build_config.spec" -ForegroundColor Red
    exit 1
}

# Create startup shortcut
Write-Host "Creating startup shortcut..." -ForegroundColor Yellow
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "$InstallDir\$AppName"
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.Description = "MAC Address Converter - Auto-format MAC addresses"
$Shortcut.Save()
Write-Host "✓ Startup shortcut created" -ForegroundColor Green

# Start the application
Write-Host ""
Write-Host "Starting MAC Address Converter..." -ForegroundColor Yellow
Start-Process -FilePath "$InstallDir\$AppName"

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Installation complete!" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The MAC Address Converter is now running and will start automatically on login." -ForegroundColor Green
Write-Host ""
Write-Host "Installation location: $InstallDir" -ForegroundColor White
Write-Host "To uninstall:" -ForegroundColor White
Write-Host "  1. Delete: $InstallDir" -ForegroundColor White
Write-Host "  2. Delete: $ShortcutPath" -ForegroundColor White
Write-Host ""
