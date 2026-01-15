from app.services.pdf_service import chunk_text

def text_chunk_text_basic():
    """Test if text is split into chunks of correct size."""

    pages = [{"page": 1, "text": "A" * 1000}] #1000 characters of 'A'

    chunks = chunk_text(pages, chunk_size = 500, overlap = 0)

    assert len(chunks) == 2
    assert len(chunks[0]["text"]) == 500
    assert chunks[0]["pages"] == 1

def test_chunk_text_overlap():
    """Test if overlap is working."""
    text = "1234567890"
    pages = [{"page": 1, "text":text}]

    #chunk size 5, overlap 2.
    #chunk 1: "12345"
    #chunk 2: "45678"
    chunks = chunk_text(pages, chunk_size = 5, overlap = 2)

    assert chunks[0]["text"] == "12345"
    assert chunks[1]["text"] == "45678"