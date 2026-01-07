from pypdf import PdfReader


def load_pdf_text(file_path: str) -> list[str]:
    reader = PdfReader(file_path)
    text_chunks = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_chunks.append(text.strip())

    return text_chunks