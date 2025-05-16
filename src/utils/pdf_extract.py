from PyPDF2 import PdfReader
from collections import Counter

def extract_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    return [page.extract_text() or "" for page in reader.pages]

def extract_metadata(pdf_file):
    reader = PdfReader(pdf_file)
    meta = reader.metadata
    return {
        "Title": meta.title,
        "Author": meta.author,
        "Subject": meta.subject,
        "Producer": meta.producer,
        "CreationDate": meta.creation_date
    }

def extract_header_footer(pages):
    header_counter = Counter()
    footer_counter = Counter()

    for page in pages:
        lines = page.splitlines()
        if not lines:
            continue
        header_counter[lines[0].strip()] += 1
        footer_counter[lines[-1].strip()] += 1

    header_lines = [line for line, count in header_counter.items() if count > 1]
    footer_lines = [line for line, count in footer_counter.items() if count > 1]

    return header_lines, footer_lines

def clean_page_text(text, headers, footers):
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped in headers or stripped in footers:
            continue
        cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines)
