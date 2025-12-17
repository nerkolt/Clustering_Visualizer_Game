@echo off
setlocal

REM Usage:
REM   build_exe.bat onedir
REM   build_exe.bat onefile
REM Default: onedir

set MODE=%1
if "%MODE%"=="" set MODE=onedir
set NAME=KmeansGame

echo Building %NAME% (%MODE%)...

python -m pip install --upgrade pip
python -m pip install pyinstaller

set ENTRY=Scripts\Kmeans_Game_Debug.py

if /I "%MODE%"=="onefile" (
  python -m PyInstaller --noconfirm --clean --windowed --onefile --name %NAME% --paths Scripts %ENTRY%
  echo Done. Output: dist\%NAME%.exe
) else (
  python -m PyInstaller --noconfirm --clean --windowed --name %NAME% --paths Scripts %ENTRY%
  echo Done. Output: dist\%NAME%\%NAME%.exe
)

endlocal


