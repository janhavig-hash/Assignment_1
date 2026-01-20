import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from app.services.embedding import embed_texts, embed_query

# --- TEST 1: Document Embedding (embed_texts) ---
@patch("app.services.embedding.ollama.embeddings")
def test_embed_texts_success(mock_ollama):
    """Test normal document embedding with 'search_document:' prefix."""
    
    # 1. Setup the Mock to return fake data
    # The ollama library returns a dict like {'embedding': [...]}
    mock_ollama.return_value = {"embedding": [0.1, 0.2, 0.3]}

    # 2. Call the function
    texts = ["Tax Report"]
    results = embed_texts(texts)

    # 3. Verify Results
    assert len(results) == 1
    assert results[0] == [0.1, 0.2, 0.3]

    # 4. CRITICAL: Check if the prefix was added correctly
    # We inspect the arguments passed to the mock
    mock_ollama.assert_called_once()
    call_args = mock_ollama.call_args
    # call_args[1] holds the keyword arguments (kwargs)
    assert call_args[1]['prompt'] == "search_document: Tax Report"
    assert call_args[1]['model'] == "nomic-embed-text"

# --- TEST 2: Query Embedding (embed_query) ---
@patch("app.services.embedding.ollama.embeddings")
def test_embed_query_success(mock_ollama):
    """Test query embedding with 'search_query:' prefix."""
    
    mock_ollama.return_value = {"embedding": [0.9, 0.8, 0.7]}

    # Call function
    result = embed_query("How much tax?")

    # Verify result
    assert result == [0.9, 0.8, 0.7]

    # Verify Prefix
    call_args = mock_ollama.call_args
    assert call_args[1]['prompt'] == "search_query: How much tax?"

# --- TEST 3: Validation Logic ---
def test_embed_texts_empty_input():
    """Should raise 400 if input list is empty."""
    with pytest.raises(HTTPException) as exc:
        embed_texts([])
    assert exc.value.status_code == 400
    assert "No text provided" in str(exc.value.detail)

@patch("app.services.embedding.ollama.embeddings")
def test_embed_texts_api_failure(mock_ollama):
    """Should raise 500 if Ollama fails."""
    # Simulate an error (e.g., Ollama is down)
    mock_ollama.side_effect = Exception("Ollama Down")

    with pytest.raises(HTTPException) as exc:
        embed_texts(["Hello"])
    
    assert exc.value.status_code == 500
    assert "Embedding generation failed" in str(exc.value.detail)