#!/usr/bin/env python3
"""
Command-line interface for PDF merger.
Usage: python cli.py file1.pdf file2.pdf file3.pdf
"""

import sys
import os
import argparse
from pathlib import Path
from pdf_merge_logic import merge_pdfs


def get_next_filename(base_name="merged_pdf"):
    """
    Generate the next available filename with counter.
    Returns: str - The next available filename
    """
    counter = 1
    while True:
        filename = f"{base_name}_{counter}.pdf"
        if not os.path.exists(filename):
            return filename
        counter += 1


def validate_pdf_files(pdf_files):
    """
    Validate that all provided files exist and are PDFs.
    Returns: list - List of valid PDF file paths
    """
    valid_files = []
    for file_path in pdf_files:
        if not os.path.exists(file_path):
            print(f"Warning: File '{file_path}' does not exist. Skipping.")
            continue
        
        if not file_path.lower().endswith('.pdf'):
            print(f"Warning: File '{file_path}' is not a PDF. Skipping.")
            continue
        
        valid_files.append(file_path)
    
    return valid_files


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple PDF files into a single PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py file1.pdf file2.pdf file3.pdf
  python cli.py *.pdf
  python cli.py "path/to/file1.pdf" "path/to/file2.pdf"
        """
    )
    
    parser.add_argument(
        'pdf_files',
        nargs='+',
        help='List of PDF files to merge (in order)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output filename (default: auto-generated with counter)'
    )
    
    args = parser.parse_args()
    
    # Validate input files
    valid_files = validate_pdf_files(args.pdf_files)
    
    if not valid_files:
        print("Error: No valid PDF files provided.")
        sys.exit(1)
    
    if len(valid_files) < 2:
        print("Error: At least 2 PDF files are required for merging.")
        sys.exit(1)
    
    # Determine output filename
    if args.output:
        output_filename = args.output
        if not output_filename.lower().endswith('.pdf'):
            output_filename += '.pdf'
    else:
        output_filename = get_next_filename()
    
    try:
        print(f"Merging {len(valid_files)} PDF files...")
        print(f"Files to merge: {', '.join(valid_files)}")
        print(f"Output file: {output_filename}")
        
        merge_pdfs(valid_files, output_filename)
        
        print(f"Successfully merged PDFs into '{output_filename}'")
        
    except Exception as e:
        print(f"Error merging PDFs: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 