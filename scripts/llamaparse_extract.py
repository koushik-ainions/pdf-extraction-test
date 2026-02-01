from llama_parse import LlamaParse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


PDF_DIR = Path("pdfs")
OUT_DIR = Path("outputs/llamaparse")
OUT_DIR.mkdir(parents=True, exist_ok=True)

parser = LlamaParse(
    result_type="markdown",   # markdown or text
    premium_mode=False        # keep cost low
)

for pdf in PDF_DIR.glob("*.pdf"):
    print(f"Processing {pdf.name}")

    docs = parser.load_data(str(pdf))

    # LlamaParse returns chunks
    combined_md = "\n\n".join(doc.text for doc in docs)

    out_file = OUT_DIR / f"{pdf.stem}.md"
    out_file.write_text(combined_md)
