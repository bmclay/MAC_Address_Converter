# Build script for MAC Address Converter (Windows)
# Usage:
#   .\build.ps1          # Build for Windows
#   .\build.ps1 -Pack    # Build and create release zip

param(
    [switch]$Pack
)

$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DistDir = Join-Path $ProjectDir "dist"
$BuildDir = Join-Path $ProjectDir "build"
$OSDir = Join-Path $DistDir "windows"

Write-Host "Building for: Windows" -ForegroundColor Cyan

# Clean previous build artifacts
if (Test-Path $BuildDir) { Remove-Item $BuildDir -Recurse -Force }
if (Test-Path $OSDir) { Remove-Item $OSDir -Recurse -Force }
New-Item -ItemType Directory -Force -Path $OSDir | Out-Null

# Run PyInstaller
Write-Host "Running PyInstaller..." -ForegroundColor Yellow
pyinstaller "$ProjectDir\build_config.spec" --distpath $OSDir --workpath $BuildDir --noconfirm
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed" }

# Assemble distribution package
Write-Host "Assembling distribution package..." -ForegroundColor Yellow
Copy-Item "$ProjectDir\scripts\windows\install.ps1" -Destination $OSDir
Copy-Item "$ProjectDir\scripts\windows\uninstall.ps1" -Destination $OSDir
if (Test-Path "$ProjectDir\assets\icon.ico") {
    Copy-Item "$ProjectDir\assets\icon.ico" -Destination $OSDir
}

if ($Pack) {
    Write-Host "Creating release archive..." -ForegroundColor Yellow
    $ZipPath = Join-Path $DistDir "mac-address-converter-windows.zip"
    if (Test-Path $ZipPath) { Remove-Item $ZipPath }
    Compress-Archive -Path $OSDir -DestinationPath $ZipPath
    Write-Host "Archive: $ZipPath" -ForegroundColor Green
}

Write-Host ""
Write-Host "Build complete! Output: $OSDir" -ForegroundColor Green
Get-ChildItem $OSDir
