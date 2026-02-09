# Uninstall script for MAC Address Converter (Windows)
# Run with: powershell -ExecutionPolicy Bypass -File uninstall.ps1

$ErrorActionPreference = "Stop"

$AppName = "mac-address-converter"
$InstallDir = Join-Path -Path $env:LOCALAPPDATA -ChildPath 'MACAddressConverter'
$StartupDir = Join-Path -Path $env:APPDATA -ChildPath 'Microsoft\Windows\Start Menu\Programs\Startup'
$ShortcutPath = Join-Path -Path $StartupDir -ChildPath 'MAC Address Converter.lnk'

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "MAC Address Converter - Windows Uninstaller" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Stop any running instances
Write-Host "Stopping any running instances..." -ForegroundColor Yellow
Get-Process -Name $AppName -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 1
Write-Host "  Done" -ForegroundColor Green

# Remove startup shortcut
if (Test-Path $ShortcutPath) {
    Write-Host "Removing startup shortcut..." -ForegroundColor Yellow
    Remove-Item $ShortcutPath -Force
    Write-Host "  Startup shortcut removed" -ForegroundColor Green
}

# Remove legacy startup batch file if present
$LegacyBat = Join-Path -Path $StartupDir -ChildPath 'start_mac_address_converter.bat'
if (Test-Path $LegacyBat) {
    Remove-Item $LegacyBat -Force
}

# Remove installation directory
if (Test-Path $InstallDir) {
    Write-Host "Removing installation directory..." -ForegroundColor Yellow
    Remove-Item $InstallDir -Recurse -Force
    Write-Host "  Installation directory removed" -ForegroundColor Green
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Uninstall complete!" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
