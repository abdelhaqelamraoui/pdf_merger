REM This script builds the Python application using PyInstaller.
pyinstaller --noconfirm --onefile --windowed --icon=icon.ico main.py
REM rename the output file to PDF-Merger.exe
if exist dist\main.exe (
    move /Y dist\main.exe dist\PDF-Merger.exe
) else (
    echo Build failed. Please check the output for errors.
)