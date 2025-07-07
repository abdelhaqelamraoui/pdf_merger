# PDF Merger

## Download

[![Download for Windows](https://img.shields.io/badge/Download-Windows%20Executable-blue?logo=windows)](dist/PDF-Merger.exe)

---

A lightweight, user-friendly Python app to merge PDF files with a modern Windows-style interface.

## Features

-  Select and reorder multiple PDF files
-  Merge PDFs with a single click
-  Choose where to save the merged file
-  Open the merged PDF after creation

## Installation (for Developers)

1. Clone this repository:
   ```bash
   git clone https://github.com/abdelhaqelamraoui/pdf_merger.git
   cd pdf_merger
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python ui.py
   ```

## Usage

-  Click **Add PDFs** to select files
-  Reorder with drag-and-drop or the up/down buttons
-  Click **Merge PDFs** and choose a save location
-  Optionally open the merged PDF after creation

## Build as Executable

To build your own Windows executable:

```bash
pip install pyinstaller
./build
```

The output will be in the `dist/` folder.

## Credits

-  **By [Abdelhaq El Amraoui](https://github.com/abdelhaqelamraoui/pdf_merger)**
-  Built with [PyPDF2](https://pypi.org/project/PyPDF2/) and [Tkinter](https://docs.python.org/3/library/tkinter.html)
