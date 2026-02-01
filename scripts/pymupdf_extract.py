import pymupdf4llm
# import pymupdf
import fitz as pymupdf
import re
from pathlib import Path

PDF_DIR = Path("pdfs")
OUT_DIR = Path("outputs/pymupdf")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def detect_repeated_patterns(text: str, min_occurrences: int = 3) -> list:
    """
    Detect text patterns that repeat multiple times across the document.
    These are likely page headers/footers.
    
    Args:
        text: Full document text
        min_occurrences: Minimum times a pattern must appear to be considered a header
        
    Returns:
        List of detected repeated patterns (likely headers/footers)
    """
    lines = text.split('\n')
    
    # Track bold text patterns that might be headers (starting with **)
    bold_patterns = {}
    
    for line in lines:
        # Look for bold text that could be page headers
        if line.strip().startswith('**') and line.strip().endswith('**'):
            clean_line = line.strip()
            bold_patterns[clean_line] = bold_patterns.get(clean_line, 0) + 1
    
    # Find patterns that repeat often (likely headers/footers)
    repeated_headers = [
        pattern for pattern, count in bold_patterns.items() 
        if count >= min_occurrences
    ]
    
    return repeated_headers


def detect_split_paragraphs(text: str, repeated_headers: list) -> list:
    """
    Detect where paragraphs (especially italic text) are split by page headers or column breaks.
    
    Args:
        text: Full document text
        repeated_headers: List of known repeated header patterns
        
    Returns:
        List of tuples with split information
    """
    splits = []
    lines = text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if current line is italic text ending with underscore (not a heading)
        if line.startswith('_') and line.endswith('_') and '**' not in line:
            # Look ahead for interruptions
            j = i + 1
            header_block = []
            section_heading_lines = []
            
            # Skip blank lines
            while j < len(lines) and not lines[j].strip():
                j += 1
            
            # Check if we hit a repeated header OR an unrelated section heading
            found_interruption = False
            
            while j < len(lines):
                next_line = lines[j].strip()
                
                # Check if this is a repeated header line
                if repeated_headers and any(header in next_line for header in repeated_headers):
                    header_block.append(next_line)
                    found_interruption = True
                    j += 1
                # Check if this is a glossary term heading that interrupts (bold+italic: _**...**_)
                elif next_line.startswith('_**') and next_line.endswith('**_'):
                    # This could be a section heading interrupting the paragraph
                    section_heading_lines.append(next_line)
                    found_interruption = True
                    j += 1
                elif not next_line:
                    j += 1
                else:
                    break
            
            if found_interruption:
                # Collect all continuation lines until paragraph ends
                continuation_lines = []
                while j < len(lines):
                    next_line = lines[j].strip()
                    if next_line and next_line.startswith('_') and next_line.endswith('_') and '**' not in next_line:
                        continuation_lines.append(next_line)
                        j += 1
                    elif not next_line and continuation_lines:
                        # End of paragraph
                        break
                    elif not next_line:
                        j += 1
                    else:
                        break
                
                # Found a split if we have continuation
                if continuation_lines:
                    splits.append({
                        'before': line,
                        'headers': '\n'.join(header_block) if header_block else '',
                        'section_heading': '\n'.join(section_heading_lines) if section_heading_lines else None,
                        'continuation': '\n'.join(continuation_lines),
                        'line_num': i
                    })
        
        i += 1
    
    return splits


def remove_repeated_headers(text: str) -> str:
    """
    Dynamically detect and remove repeated page headers/footers that split paragraphs.
    Also fixes paragraphs split by column-break artifacts (unrelated section headings).
    Preserves legitimate section headings by moving them after the complete paragraph.
    """
    # Step 1: Detect repeated patterns (headers/footers)
    repeated_headers = detect_repeated_patterns(text, min_occurrences=2)
    
    # Step 2: Detect split paragraphs (works even if no repeated headers)
    splits = detect_split_paragraphs(text, repeated_headers)
    
    if not splits and not repeated_headers:
        # Nothing to fix
        return text
    
    # Step 3: Fix each split by removing headers and merging text
    fixed_text = text
    
    for split in reversed(splits):  # Process in reverse to maintain positions
        before = split['before']
        headers = split['headers']
        section_heading = split['section_heading']
        continuation = split['continuation']
        
        # Build the search pattern - need to match the entire block
        if section_heading and headers:
            # Pattern with both headers and section heading
            search_pattern = re.escape(before) + r'\s+' + \
                           re.escape(headers) + r'\s+' + \
                           re.escape(section_heading) + r'\s+' + \
                           re.escape(continuation)
            
            # Replacement: merge text, then add section heading after complete paragraph
            replacement = before + '\n' + continuation + '\n\n' + section_heading + '\n'
            fixed_text = re.sub(search_pattern, replacement, fixed_text, count=1, flags=re.MULTILINE)
        elif section_heading:
            # Pattern with only section heading (column break artifact)
            search_pattern = re.escape(before) + r'\s+' + \
                           re.escape(section_heading) + r'\s+' + \
                           re.escape(continuation)
            
            # Replacement: merge text, then add section heading after complete paragraph
            replacement = before + '\n' + continuation + '\n\n' + section_heading + '\n'
            fixed_text = re.sub(search_pattern, replacement, fixed_text, count=1, flags=re.MULTILINE)
        elif headers:
            # Pattern with only headers (no section heading)
            search_pattern = re.escape(before) + r'\s+' + \
                           re.escape(headers) + r'\s+' + \
                           re.escape(continuation)
            
            replacement = before + '\n' + continuation
            fixed_text = re.sub(search_pattern, replacement, fixed_text, count=1, flags=re.MULTILINE)
    
    # Fallback: Remove remaining repeated headers that weren't part of splits
    if repeated_headers:
        for header in repeated_headers:
            # Remove standalone headers (not caught by split detection)
            pattern = r'\n+' + re.escape(header) + r'\n+'
            fixed_text = re.sub(pattern, '\n\n', fixed_text)
    
    return fixed_text


def clean_formatting(text: str) -> str:
    """
    Clean up formatting issues and improve text structure.
    """
    # Remove strikethrough markers (~~text~~) - these come from PDF formatting
    # Handle ~~text with spaces~~ pattern (greedy to get all content between markers)
    text = re.sub(r'~~([^~]*?)~~', r'\1', text)
    # Remove any remaining standalone ~~ markers
    text = re.sub(r'~~', '', text)
    
    # Remove HTML line breaks that appear in tables and text
    text = re.sub(r'<br>', ' ', text)  # Replace with space to preserve word separation
    text = re.sub(r'<br\s*/>', ' ', text)  # Also handle self-closing variant
    
    # Fix broken italic paragraphs - merge lines that are part of same italic block
    # Pattern: _text at end of line_\n_text at start of next line_
    # This happens when PDF has italicized paragraphs broken across lines
    while re.search(r'_([^\n_]+)_\s*\n\s*_', text):
        text = re.sub(r'_([^\n_]+)_\s*\n\s*_', r'_\1 ', text)
    
    # Fix headings incorrectly appended to end of paragraphs
    # Pattern: procedures. **CHIEF**_ _**INFORMATION** **OFFICERS**_ _**AND**...
    # This matches: period/punctuation followed by bold all-caps heading fragments
    text = re.sub(r'([.!?])\s+(\*\*[A-Z][A-Z\s]+\*\*_(?:\s+_\*\*[A-Z][A-Z\s]+\*\*_)*)', r'\1\n\n_\2', text)
    
    # Aggressive line merging to fix broken paragraphs
    lines = text.split('\n')
    merged_lines = []
    i = 0
    
    while i < len(lines):
        current_line = lines[i]
        current_stripped = current_line.strip()
        
        # Skip empty lines for now, we'll clean them up later
        if not current_stripped:
            merged_lines.append(current_line)
            i += 1
            continue
        
        # Try to merge with following non-empty lines
        merged_text = current_line
        j = i + 1
        
        while j < len(lines):
            next_line = lines[j]
            next_stripped = next_line.strip()
            
            # If next line is empty, check if there's a continuation after
            if not next_stripped:
                # Look ahead to see if there's continuation text
                if j + 1 < len(lines):
                    continuation = lines[j + 1].strip()
                    # If continuation exists and doesn't start with special markers
                    if (continuation and 
                        not continuation.startswith(('#', '-', '*', '|', '_**', '`o`')) and
                        not re.match(r'^\d+\.', continuation) and
                        not merged_text.rstrip().endswith(('.', '!', '?', ':')) and
                        '|---|' not in merged_text):
                        # Skip the blank line and continue merging
                        j += 1
                        continue
                # Otherwise, stop merging
                break
            
            # Check if we should merge this line
            next_indent = len(next_line) - len(next_line.lstrip())
            current_indent = len(merged_text) - len(merged_text.lstrip())
            
            should_not_merge = (
                merged_text.rstrip().endswith(('.', '!', '?', ':')) or
                next_stripped.startswith(('#', '-', '*', '|', '_**', '`o`')) or
                re.match(r'^\d+\.', next_stripped) or
                '|---|' in next_line or
                abs(next_indent - current_indent) > 2
            )
            
            if should_not_merge:
                break
            
            # Merge the line
            merged_text = merged_text.rstrip() + ' ' + next_line.lstrip()
            j += 1
        
        merged_lines.append(merged_text)
        i = j
    
    text = '\n'.join(merged_lines)
    
    # Fix bullet points that have unnecessary italic formatting
    # Pattern: - _italic bullet text_
    text = re.sub(r'(\n\s+- )_([^_\n]+)_', r'\1\2', text)
    
    # Clean up excessive blank lines - reduce to single blank line between paragraphs
    # Replace 3 or more newlines with exactly 2 (one blank line)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Fix spacing around headers (ensure proper separation)
    text = re.sub(r'\n(#{1,6} .+)\n', r'\n\n\1\n\n', text)
    
    # Remove trailing whitespace from lines
    text = re.sub(r'[ \t]+\n', '\n', text)
    
    # Fix hyphenated words split across lines (remove hyphen + newline)
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    
    return text


def improve_table_formatting(text: str) -> str:
    """
    Improve table formatting in markdown.
    """
    # Ensure tables have proper spacing before and after
    text = re.sub(r'([^\n])\n(\|[^\n]+\|)', r'\1\n\n\2', text)
    text = re.sub(r'(\|[^\n]+\|)\n([^\n|])', r'\1\n\n\2', text)
    
    return text


def fix_heading_position(text: str) -> str:
    """
    Fix misplaced headings that appear after their content instead of before.
    Pattern: 
        Some content text starting here
        _**HEADING TEXT**_
        rest of content text
    Should become:
        _**HEADING TEXT**_
        Some content text starting here
        rest of content text
    """
    # Pattern: any line that's NOT a term heading, followed by the term heading
    # Using negative lookahead (?!_\*\*) to exclude lines that are term headings
    pattern = r'(\n)((?!_\*\*)[^\n]+\n)(_\*\*[A-Z][A-Z0-9\s\-\(\)\/]+\*\*_)\n'
    
    def reorder_match(match):
        newline = match.group(1)
        content_start = match.group(2)
        heading = match.group(3)
        # Put the heading before the content text
        return f'{newline}{heading}\n{content_start}'
    
    # Apply the fix iteratively until no more matches
    fixed_text = text
    prev_text = ""
    while prev_text != fixed_text:
        prev_text = fixed_text
        fixed_text = re.sub(pattern, reorder_match, fixed_text)
    
    # Also clean up javascript links that shouldn't be there
    fixed_text = re.sub(r'\[([^\]]+)\]\(javascript:[^\)]+\)', r'\1', fixed_text)
    
    return fixed_text


for pdf in PDF_DIR.glob("*.pdf"):
    print(f"Processing {pdf.name}")
    
    # Remove existing output files for this PDF if they exist
    existing_files = list(OUT_DIR.glob(f"{pdf.stem}*"))
    if existing_files:
        print(f"  → Removing {len(existing_files)} existing output files...")
        for existing_file in existing_files:
            existing_file.unlink()
    
    # Open document for better control
    doc = pymupdf.open(str(pdf))
    
    # Use TOC-based header detection if available (more accurate)
    try:
        toc_info = pymupdf4llm.TocHeaders(doc)
    except:
        toc_info = None
    
    # Extract with improved settings for structure
    md_text = pymupdf4llm.to_markdown(
        doc,
        hdr_info=toc_info,  # Use TOC for headers if available
        table_strategy="lines_strict",  # Better table detection
        ignore_code=False,  # Preserve formatting
        margins=(0, 72, 0, 72),  # Ignore top/bottom margins (headers/footers) - 72 points = 1 inch
        page_chunks=False,  # Get single continuous text
        write_images=False,  # Don't extract images
        show_progress=True,  # Show progress
    )
    
    doc.close()
    
    print(f"  → Extracted {len(md_text)} characters")
    
    # Post-process to fix issues
    md_text = remove_repeated_headers(md_text)        # Remove page headers interrupting paragraphs
    md_text = fix_heading_position(md_text)           # Fix headings appearing after their content
    md_text = clean_formatting(md_text)               # Clean up formatting issues
    md_text = improve_table_formatting(md_text) # Improve table spacing

    out_file = OUT_DIR / f"{pdf.stem}.md"
    out_file.write_text(md_text)
    print(f"  ✓ Saved: {out_file}")
