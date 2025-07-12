@echo off
REM PDF Merger Command Line Interface
REM Usage: merge_pdfs.bat file1.pdf file2.pdf file3.pdf

if "%~1"=="" (
    echo Usage: merge_pdfs.bat file1.pdf file2.pdf file3.pdf
    echo.
    echo Examples:
    echo   merge_pdfs.bat document1.pdf document2.pdf
    echo   merge_pdfs.bat *.pdf
    echo   merge_pdfs.bat "path\to\file1.pdf" "path\to\file2.pdf"
    exit /b 1
)

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%cli.py" %* 