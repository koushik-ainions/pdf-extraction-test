from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorOptions
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from pathlib import Path

PDF_DIR = Path("pdfs")
OUT_DIR = Path("outputs/docling")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Fast pipeline configuration
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = False  # Disable OCR for speed (enable if scanned docs)
pipeline_options.do_table_structure = True  # Keep table structure
pipeline_options.generate_page_images = False
pipeline_options.generate_picture_images = False

# Use multiple threads for faster processing
pipeline_options.accelerator_options = AcceleratorOptions(
    num_threads=8,  # Increase threads for speed
)

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_cls=StandardPdfPipeline,
            pipeline_options=pipeline_options,
        )
    }
)

for pdf in PDF_DIR.glob("*.pdf"):
    print(f"Processing {pdf.name}...")
    
    # Remove existing output files for this PDF if they exist
    existing_files = list(OUT_DIR.glob(f"{pdf.stem}*"))
    if existing_files:
        print(f"  → Removing {len(existing_files)} existing output files...")
        for existing_file in existing_files:
            existing_file.unlink()
    
    result = converter.convert(pdf)
    doc = result.document

    # Markdown output with proper table formatting
    md_path = OUT_DIR / f"{pdf.stem}.md"
    doc.save_as_markdown(md_path)
    print(f"  ✓ Saved markdown: {md_path}")

    # JSON with full document structure preserved
    json_path = OUT_DIR / f"{pdf.stem}.json"
    doc.save_as_json(json_path)
    print(f"  ✓ Saved JSON: {json_path}")

    # HTML output for better structure visualization
    html_path = OUT_DIR / f"{pdf.stem}.html"
    doc.save_as_html(html_path)
    print(f"  ✓ Saved HTML: {html_path}")
    print()
