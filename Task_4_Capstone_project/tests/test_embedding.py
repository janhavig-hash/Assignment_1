from unittest.mock import patch
from app.services.embedding import embed_query, embed_texts

@patch("app.services.embedding.ollama.embeddings")
def test_embed_query_adds_prefix(mock_ollama):
    """Test if 'search_query:' prefix is added automatically."""
    
    mock_ollama.return_value = {"embedding": [0.1, 0.2, 0.3]}
    
    question = "what is my tax?"
    embed_query(question)
    
    args, kwargs = mock_ollama.call_args
    sent_prompt = kwargs["prompt"]
    
    # --- FIX: Match the lowercase 'w' from the input ---
    assert sent_prompt == "search_query: what is my tax?"  

@patch("app.services.embedding.ollama.embeddings")
def test_embed_texts_adds_prefix(mock_ollama):
    """Test if 'search_document:' prefix is added to documents."""
    
    mock_ollama.return_value = {"embedding": [0.1, 0.2, 0.3]}
    
    texts = ["Tax Report 2024"]
    embed_texts(texts)
    
    args, kwargs = mock_ollama.call_args
    sent_prompt = kwargs["prompt"]
    
    assert sent_prompt == "search_document: Tax Report 2024"