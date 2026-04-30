param(
  [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

& $Python -m pip install --upgrade pip
& $Python -m pip install -e . pyinstaller

& $Python -m PyInstaller `
  --noconfirm `
  --clean `
  --name PE3Generator `
  --windowed `
  --onefile `
  --collect-all openpyxl `
  -m pe3_generator.gui

Write-Host "Build completed. EXE: dist/PE3Generator.exe"
