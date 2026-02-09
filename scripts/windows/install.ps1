# Installation script for MAC Address Converter (Windows)
# Run with: powershell -ExecutionPolicy Bypass -File install.ps1

$ErrorActionPreference = "Stop"

# Resolve script directory so paths work regardless of where it's run from
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$AppName = "mac-address-converter.exe"
$InstallDir = Join-Path -Path $env:LOCALAPPDATA -ChildPath 'MACAddressConverter'
$StartupDir = Join-Path -Path $env:APPDATA -ChildPath 'Microsoft\Windows\Start Menu\Programs\Startup'
$ShortcutPath = Join-Path -Path $StartupDir -ChildPath 'MAC Address Converter.lnk'

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "MAC Address Converter - Windows Installer" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Stop any existing running instances
Write-Host "Stopping any running instances..." -ForegroundColor Yellow
Get-Process -Name "mac-address-converter" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 1
Write-Host "✓ Done" -ForegroundColor Green

# Remove legacy startup batch file if present
$LegacyBat = Join-Path -Path $StartupDir -ChildPath 'start_mac_address_converter.bat'
if (Test-Path $LegacyBat) {
    Write-Host "Removing legacy startup script..." -ForegroundColor Yellow
    Remove-Item $LegacyBat -Force
    Write-Host "✓ Legacy startup script removed" -ForegroundColor Green
}

# Create installation directory
Write-Host "Creating installation directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

# Copy the executable (located next to this script in the dist package)
$ExePath = Join-Path -Path $ScriptDir -ChildPath $AppName
if (Test-Path $ExePath) {
    Write-Host "Installing executable to $InstallDir..." -ForegroundColor Yellow
    Copy-Item $ExePath -Destination $InstallDir -Force
    Write-Host "✓ Executable installed" -ForegroundColor Green
} else {
    Write-Host "Error: Executable not found at $ExePath" -ForegroundColor Red
    Write-Host "Please build the application first with: .\build.ps1" -ForegroundColor Red
    exit 1
}

# Create startup shortcut
Write-Host "Creating startup shortcut..." -ForegroundColor Yellow
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = (Join-Path -Path $InstallDir -ChildPath $AppName)
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.Description = "MAC Address Converter - Auto-format MAC addresses"
$Shortcut.Save()
Write-Host "✓ Startup shortcut created" -ForegroundColor Green

# Start the application
Write-Host ""
Write-Host "Starting MAC Address Converter..." -ForegroundColor Yellow
Start-Process -FilePath (Join-Path -Path $InstallDir -ChildPath $AppName)

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
