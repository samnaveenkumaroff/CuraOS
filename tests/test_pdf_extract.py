import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.pdf_extract import (
    extract_text_from_pdf,
    extract_metadata_from_pdf,
    extract_header_footer,
    clean_text
)

def test_pdf_extraction(pdf_path):
    print("\n📄 Testing PDF Extraction Functions on:", pdf_path)

    # 1. Extract full text
    pages = extract_text_from_pdf(pdf_path)
    print(f"\n📝 Total Pages Extracted: {len(pages)}")
    for i, page_text in enumerate(pages):
        print(f"\n--- Page {i+1} (First 300 chars) ---\n{page_text[:300]}")

    # 2. Extract metadata
    metadata = extract_metadata_from_pdf(pdf_path)
    print("\n📌 Metadata Extracted:")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    # 3. Extract header/footer from first page
    if pages:
        header, footer = extract_header_footer(pages[0])
        print("\n📚 Header (first 2 lines):", header)
        print("📄 Footer (last 2 lines):", footer)

    # 4. Clean first page text
    if pages:
        cleaned = clean_text(pages[0])
        print("\n🧹 Cleaned First Page Text (first 300 chars):")
        print(cleaned[:300])

if __name__ == "__main__":
    sample_pdf_path = "../data/Sample Document.pdf"  # Adjust path as needed
    if os.path.exists(sample_pdf_path):
        test_pdf_extraction(sample_pdf_path)
    else:
        print(f"❌ PDF file not found at {sample_pdf_path}")
