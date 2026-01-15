import io
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@patch("app.api.upload.extract_text_from_pdf")
@patch("app.api.upload.embed_texts")
@patch("app.api.upload.store_chunks")
def test_upload_pdf(mock_store, mock_embed, mock_extract):
    """
    Test the PDF upload flow.
    """
    # 1. Mock Extraction
    mock_extract.return_value = [
        {"page": 1, "text": "Sample content chunk 1"},
        {"page": 1, "text": "Sample content chunk 2"}
    ]
    
    # 2. Mock Embedding
    mock_embed.return_value = [[0.1, 0.1], [0.2, 0.2]]
    
    # 3. Mock Storage
    mock_store.return_value = None
    
    # Create a fake PDF file in memory
    file_content = b"%PDF-1.4 fake pdf content"
    file = {"file": ("test.pdf", io.BytesIO(file_content), "application/pdf")}
    
    response = client.post("/api/upload", files=file)
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"

@patch("app.api.query.embed_query")
@patch("app.api.query.collection") 
@patch("app.api.query.generate_answer")
def test_query_docs(mock_generate, mock_collection, mock_embed):
    """
    Test the query endpoint.
    """
    # 1. Mock Embedding
    mock_embed.return_value = [0.1, 0.2]
    
    # 2. Mock Vector Search Result
    mock_collection.query.return_value = {
        "documents": [["Taxable income is 5 lakhs"]],
        "metadatas": [[{"page": 1, "source": "test.pdf"}]]
    }
    
    # 3. Mock LLM Answer
    mock_generate.return_value = "Your taxable income is 5 lakhs."
    
    payload = {"question": "What is my income?"}
    response = client.post("/api/query", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Your taxable income is 5 lakhs."