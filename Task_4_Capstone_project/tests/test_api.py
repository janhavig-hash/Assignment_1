import pytest
from unittest.mock import patch

# --- TEST UPLOAD ENDPOINT ---
@patch("app.api.upload.store_chunks")       # Mock DB storage
@patch("app.api.upload.embed_texts")        # Mock Embedding
@patch("app.api.upload.extract_text_from_pdf") # Mock PDF reading
def test_upload_flow(mock_extract, mock_embed, mock_store, client):
    # Setup Mocks
    mock_extract.return_value = [{"text": "Sample", "page": 1}]
    mock_embed.return_value = [[0.1, 0.2]]
    mock_store.return_value = True

    # Fake File Upload
    files = {"file": ("test.pdf", b"PDF_CONTENT", "application/pdf")}
    data = {"session_id": "session_123"}

    response = client.post("/api/upload", files=files, data=data)

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    # Verify session_id was passed correctly
    mock_store.assert_called_once()
    assert mock_store.call_args[1]["session_id"] == "session_123"

# --- TEST QUERY ENDPOINT ---
@patch("app.api.query.generate_answer")
@patch("app.api.query.embed_query")
@patch("app.services.vector_store.search_similar")
def test_query_flow(mock_search, mock_embed, mock_llm, client):
    # Setup Mocks
    mock_embed.return_value = [0.1, 0.2]
    mock_search.return_value = {
        "documents": [["Tax info"]], 
        "metadatas": [[{"page": 1, "source": "doc.pdf"}]]
    }
    mock_llm.return_value = "Your tax is 10%."

    # Fake Query
    payload = {
        "question": "How much tax?", 
        "session_id": "session_123"
    }

    response = client.post("/api/query", json=payload)

    assert response.status_code == 200
    assert response.json()["answer"] == "Your tax is 10%."