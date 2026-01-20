import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
from app.services.vector_store import store_chunks, search_similar

# --- TEST 1: Storing Chunks ---
@patch("app.services.vector_store.collection") # Mock the global collection object
def test_store_chunks_success(mock_collection):
    """Test if data is correctly formatted for ChromaDB."""
    
    chunks = [{"text": "Hello", "page": 1, "source": "test.pdf"}]
    embeddings = [[0.1, 0.2]]
    session_id = "user_123"

    store_chunks(chunks, embeddings, session_id)

    # Verify collection.add was called
    mock_collection.add.assert_called_once()
    
    # Inspect arguments
    call_args = mock_collection.add.call_args[1] # Get keyword args
    assert call_args["documents"] == ["Hello"]
    assert call_args["embeddings"] == [[0.1, 0.2]]
    assert call_args["metadatas"][0]["session_id"] == "user_123"

def test_store_chunks_validation():
    """Test input validation logic."""
    # Empty input
    with pytest.raises(HTTPException):
        store_chunks([], [], "sess_1")
    
    # Mismatch length
    with pytest.raises(HTTPException):
        store_chunks([{"a":1}], [], "sess_1")

# --- TEST 2: Searching ---
@patch("app.services.vector_store.collection")
def test_search_similar_success(mock_collection):
    """Test if search query includes session_id filter."""
    
    # Setup Mock Result
    mock_collection.query.return_value = {
        "documents": [["Result"]],
        "metadatas": [[{"page": 1}]]
    }

    results = search_similar([0.1, 0.2], session_id="user_123")

    # CRITICAL: Verify the filter was applied
    mock_collection.query.assert_called_once()
    call_args = mock_collection.query.call_args[1]
    
    # Check if 'where={"session_id": ...}' was passed
    assert call_args["where"] == {"session_id": "user_123"}