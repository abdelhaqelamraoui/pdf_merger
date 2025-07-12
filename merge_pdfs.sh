#!/bin/bash
# PDF Merger Command Line Interface
# Usage: ./merge_pdfs.sh file1.pdf file2.pdf file3.pdf

if [ $# -eq 0 ]; then
    echo "Usage: ./merge_pdfs.sh file1.pdf file2.pdf file3.pdf"
    echo ""
    echo "Examples:"
    echo "  ./merge_pdfs.sh document1.pdf document2.pdf"
    echo "  ./merge_pdfs.sh *.pdf"
    echo "  ./merge_pdfs.sh \"path/to/file1.pdf\" \"path/to/file2.pdf\""
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/cli.py" "$@" 