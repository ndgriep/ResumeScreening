from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document
import io

def extract_text(file: bytes, filename: str) -> str:
    if filename.endswith(".pdf"):
        return extract_pdf(file)
    elif filename.endswith(".docx"):
        return extract_docx(file)
    else:
        return file.decode("utf-8", errors="ignore")  # fallback for .txt

def extract_pdf(file: bytes) -> str:
    with io.BytesIO(file) as f:
        return extract_pdf_text(f)

def extract_docx(file: bytes) -> str:
    with io.BytesIO(file) as f:
        doc = Document(f)
        return "\n".join([p.text for p in doc.paragraphs])
