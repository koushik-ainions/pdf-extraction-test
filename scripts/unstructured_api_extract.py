from unstructured_client import UnstructuredClient
from unstructured_client.models import shared, operations
from pathlib import Path
import json
import os
from dotenv import load_dotenv
load_dotenv()

PDF_DIR = Path("pdfs")
OUT_DIR = Path("outputs/unstructured_api")
OUT_DIR.mkdir(parents=True, exist_ok=True)

client = UnstructuredClient(
    api_key_auth=os.environ["UNSTRUCTURED_API_KEY"]
)

for pdf in PDF_DIR.glob("*.pdf"):
    print(f"Processing {pdf.name}")

    with open(pdf, "rb") as f:
        data = f.read()
        
        req = operations.PartitionRequest(
            partition_parameters=shared.PartitionParameters(
                files=shared.Files(
                    content=data,
                    file_name=pdf.name,
                ),
                strategy=shared.Strategy.HI_RES,
                hi_res_model_name="yolox",
                pdf_infer_table_structure=True,
                extract_image_block_types=["Image", "Table"],
                chunking_strategy="by_title",
            )
        )
        
        response = client.general.partition(request=req)

    # Save JSON output
    json_file = OUT_DIR / f"{pdf.stem}.json"
    with open(json_file, "w") as out:
        json.dump(response.elements, out, indent=2)
    print(f"Saved JSON → {json_file}")
    
    # Convert to Markdown
    md_file = OUT_DIR / f"{pdf.stem}.md"
    with open(md_file, "w") as out:
        for element in response.elements:
            text = element.get("text", "")
            elem_type = element.get("type", "")
            
            if text.strip():
                # Add appropriate markdown formatting based on element type
                if "Title" in elem_type or "Header" in elem_type:
                    # Count heading level from metadata if available
                    level = element.get("metadata", {}).get("category_depth", 1)
                    out.write(f"{'#' * min(level, 6)} {text}\n\n")
                elif "Table" in elem_type:
                    out.write(f"{text}\n\n")
                elif "List" in elem_type:
                    # Format as list items
                    for line in text.split('\n'):
                        if line.strip():
                            out.write(f"- {line.strip()}\n")
                    out.write("\n")
                else:
                    out.write(f"{text}\n\n")
    
    print(f"Saved MD → {md_file}")
