import sys
import os
from pathlib import Path
import chardet
from weasyprint import HTML
from PyPDF2 import PdfReader, PdfWriter

def convert_html_to_pdf_with_metadata(html_file, pdf_file):
    """
    Converts an HTML file to PDF and adds custom metadata.

    Args:
        html_file (Path): Path to the input HTML file.
        pdf_file (Path): Path to the output PDF file.
    """

    # Check if output PDF exists and delete if necessary
    if pdf_file.is_file():
        print(f"File {pdf_file.name} already exists. Deleting...")
        os.remove(pdf_file)

    # Detect encoding and convert HTML to string
    with html_file.open('rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        print(f"Detected encoding: {encoding}")
        html_string = raw_data.decode(encoding, errors='replace')

    # Convert HTML string to PDF
    try:
        HTML(string=html_string).write_pdf(str(pdf_file))
        print(f"Successfully converted HTML to PDF: {pdf_file.name}")
    except Exception as e:
        print(f"Error during HTML to PDF conversion: {e}")
        sys.exit(1)

    # Add metadata to PDF
    try:
        # Read existing PDF
        pdf = PdfReader(pdf_file)
        if len(pdf.pages) == 0:
            raise Exception("PDF contains no pages.")

        # Create a new PDF object to add metadata
        writer = PdfWriter()
        for page in pdf.pages:
            writer.add_page(page)

        # Add custom metadata
        writer.add_metadata({
            '/Author': 'DevConcept',
            '/Title': 'Logisteo',
            '/Subject': 'Order nr ' + pdf_file.stem,
            '/Keywords': 'Logisteo, DevConcept',
            '/Creator': 'DevConcept Bartosz Polak',
            '/Producer': 'Bartosz Polak',
        })

        # Write to a temporary file and replace the original
        temp_pdf_file = f"{pdf_file.stem}_temp.pdf"
        with open(temp_pdf_file, "wb") as outputStream:
            writer.write(outputStream)
        os.remove(pdf_file)
        os.rename(temp_pdf_file, pdf_file)
    except Exception as e:
        print(f"Error adding metadata to PDF: {e}")
        sys.exit(1)

# Get input and output file paths from command line arguments
html_file = Path(sys.argv[1])
pdf_file = Path(sys.argv[2])

# Call the main function
convert_html_to_pdf_with_metadata(html_file, pdf_file)
