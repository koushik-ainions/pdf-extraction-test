import pypdfium2 as pdfium
from pathlib import Path

def extract_with_pypdfium2(pdf_path: str, output_path: str):
    """
    Extract text from PDF using pypdfium2.
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Path to output markdown file
    """
    print(f"Processing {Path(pdf_path).name}")
    
    markdown_content = []
    
    # Open PDF
    pdf = pdfium.PdfDocument(pdf_path)
    
    try:
        # Extract text from each page
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            
            # Get text page object
            textpage = page.get_textpage()
            
            # Extract text
            text = textpage.get_text_range()
            
            if text:
                markdown_content.append(text)
                markdown_content.append("\n\n")
            
            # Close textpage
            textpage.close()
            page.close()
    
    finally:
        pdf.close()
    
    # Write to output file
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(markdown_content))
    
    print(f"  ✓ Saved: {output_path}")

def main():
    # Setup paths
    pdf_dir = Path("pdfs")
    output_dir = Path("outputs/pypdfium2")
    
    # Get all PDFs
    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in pdfs/ directory")
        return
    
    # Clean existing output files
    if output_dir.exists():
        for file in output_dir.glob("*.md"):
            file.unlink()
            print(f"  → Removed existing file: {file.name}")
    
    # Process each PDF
    for pdf_path in pdf_files:
        output_path = output_dir / f"{pdf_path.stem}.md"
        try:
            extract_with_pypdfium2(str(pdf_path), str(output_path))
        except Exception as e:
            print(f"  ✗ Error processing {pdf_path.name}: {e}")

if __name__ == "__main__":
    main()
