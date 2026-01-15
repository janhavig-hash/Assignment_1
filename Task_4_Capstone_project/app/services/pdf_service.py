from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Union, BinaryIO

def extract_text_from_pdf(file_input: Union[str, BinaryIO]) -> list[dict]:
    """
    Reads a PDF file (path or binary stream) and extracts text.
    Returns a list of CHUNKS (not just pages).
    """
    reader = PdfReader(file_input)
    pages = []

    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append({
            "page": idx + 1,
            "text": text
        })

    # Pass the extracted pages to the chunking function
    return chunk_text(pages)

def chunk_text(pages: list[dict], chunk_size=500, overlap=50) -> list[dict]:
    """
    Splits page text into smaller overlapping chunks.
    This function is now separate so it can be tested easily.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []
    for page in pages:
        # Split the text of this specific page
        page_chunks = text_splitter.split_text(page["text"])
        
        # Add metadata (page number) to each chunk
        for chunk_text in page_chunks:
            chunks.append({
                "text": chunk_text,
                "page": page["page"]
            })
            
    return chunks