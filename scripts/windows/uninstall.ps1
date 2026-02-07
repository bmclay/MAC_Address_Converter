# Uninstallation script for MAC Address Converter (Windows)

$InstallDir = "$env:LOCALAPPDATA\MACAddressConverter"
$ShortcutPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\MAC Address Converter.lnk"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "MAC Address Converter - Uninstaller" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Kill any running instances
Write-Host "Stopping running instances..." -ForegroundColor Yellow
Get-Process -Name "mac-address-converter" -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "✓ Stopped" -ForegroundColor Green

# Remove legacy startup batch file if present
$LegacyBat = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\start_mac_address_converter.bat"
if (Test-Path $LegacyBat) {
    Write-Host "Removing legacy startup script..." -ForegroundColor Yellow
    Remove-Item $LegacyBat -Force
    Write-Host "✓ Legacy startup script removed" -ForegroundColor Green
}

# Remove startup shortcut
if (Test-Path $ShortcutPath) {
    Write-Host "Removing startup shortcut..." -ForegroundColor Yellow
    Remove-Item $ShortcutPath -Force
    Write-Host "✓ Shortcut removed" -ForegroundColor Green
}

# Remove installation directory
if (Test-Path $InstallDir) {
    Write-Host "Removing installation directory..." -ForegroundColor Yellow
    Remove-Item $InstallDir -Recurse -Force
    Write-Host "✓ Installation directory removed" -ForegroundColor Green
}

Write-Host ""
Write-Host "✓ Uninstallation complete!" -ForegroundColor Green
Write-Host ""
