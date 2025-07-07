# This script uses PyInstaller to create a standalone executable from the main.py file.
pyinstaller --noconfirm --onefile --windowed --icon=icon.ico main.py
# rename the output file to PDF-Merger
mv dist/main dist/PDF-Merger