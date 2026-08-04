import fitz  # PyMuPDF
import re

def parse_pdf_from_bytes(file_bytes: bytes) -> str:
    """
    Extracts text from a PDF file provided as bytes.
    Cleans up excessive whitespace and non-printable characters.
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text_content = []
    
    for page in doc:
        text_content.append(page.get_text("text"))
        
    raw_text = "\n".join(text_content)
    
    # Clean the text: replace multiple spaces and newlines with a single space
    cleaned_text = re.sub(r'\s+', ' ', raw_text).strip()
    return cleaned_text
