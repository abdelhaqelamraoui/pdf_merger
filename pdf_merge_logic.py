from PyPDF2 import PdfMerger

def merge_pdfs(pdf_files, output_path):
    """
    Merge the list of PDF files into a single PDF at output_path.
    Raises exception on error.
    """
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merger.write(output_path)
    merger.close() 