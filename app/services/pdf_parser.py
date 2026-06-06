import io
import pdfplumber


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_parts = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text.strip())

    full_text = "\n\n".join(text_parts)

    if not full_text.strip():
        raise ValueError("Could not extract text from PDF. The file may be scanned or image-based.")

    return full_text


def clean_text(text: str) -> str:
    lines = text.splitlines()
    cleaned = []

    for line in lines:
        stripped = line.strip()
        if stripped:
            cleaned.append(stripped)

    return "\n".join(cleaned)