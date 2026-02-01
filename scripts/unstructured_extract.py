from unstructured.partition.pdf import partition_pdf
from pathlib import Path

PDF_DIR = Path("pdfs")
OUT_DIR = Path("outputs/unstructured/local")
OUT_DIR.mkdir(parents=True, exist_ok=True)

for pdf in PDF_DIR.glob("*.pdf"):
    print(f"Processing {pdf.name}")

    elements = partition_pdf(
        filename=str(pdf),
        infer_table_structure=True,
        strategy="hi_res"
    )

    out_file = OUT_DIR / f"{pdf.stem}.txt"
    with open(out_file, "w") as f:
        for el in elements:
            f.write(f"[{el.category}]\n")
            f.write(el.text or "")
            f.write("\n\n")
