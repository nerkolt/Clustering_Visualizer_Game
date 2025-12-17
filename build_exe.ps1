param(
    [ValidateSet("onedir","onefile")]
    [string]$Mode = "onedir",
    [string]$Name = "KmeansGame"
)

$ErrorActionPreference = "Stop"

Write-Host "Building $Name ($Mode)..." -ForegroundColor Cyan

python -m pip install --upgrade pip | Out-Host
python -m pip install pyinstaller | Out-Host

# Entry script
$Entry = "Scripts\Kmeans_Game_Debug.py"

# Note: The game itself does not load images/sounds at runtime currently.
# Assets/ is only used for documentation screenshots, so we do not bundle it by default.

if ($Mode -eq "onefile") {
    python -m PyInstaller --noconfirm --clean --windowed --onefile --name $Name --paths Scripts $Entry | Out-Host
    Write-Host "Done. Output: dist\$Name.exe" -ForegroundColor Green
} else {
    python -m PyInstaller --noconfirm --clean --windowed --name $Name --paths Scripts $Entry | Out-Host
    Write-Host "Done. Output: dist\$Name\$Name.exe" -ForegroundColor Green
}


