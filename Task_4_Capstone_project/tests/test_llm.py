import pytest
from unittest.mock import patch, MagicMock
from app.services.llm import generate_answer

def test_generate_answer_empty_context():
    """
    Test 1: If no context is provided, the function should return 
    the fallback message immediately without calling the LLM.
    """
    question = "What is my tax?"
    contexts = [] # Empty list
    
    answer = generate_answer(question, contexts)
    
    # This string must match exactly what is in your llm.py
    assert answer == "The document does not contain this information."

@patch("app.services.llm.ollama.chat")
def test_generate_answer_with_context(mock_chat):
    """
    Test 2: If context exists, it should call Ollama and return the answer.
    """
    # 1. Setup the Mock AI response
    mock_response = {
        "message": {
            "content": "Your tax is 5000 (Page 1)."
        }
    }
    mock_chat.return_value = mock_response
    
    # 2. Define inputs
    question = "What is my tax?"
    contexts = [
        {"text": "Tax is 5000", "page": 1},
        {"text": "Salary is 50000", "page": 1}
    ]
    
    # 3. Call function
    answer = generate_answer(question, contexts)
    
    # 4. Verify the result
    assert answer == "Your tax is 5000 (Page 1)."
    
    # 5. Verify Ollama was actually called
    mock_chat.assert_called_once()
    
    # 6. Verify the prompt sent to Ollama contained the context info
    # We check the arguments sent to the mock
    args, kwargs = mock_chat.call_args
    sent_messages = kwargs["messages"]
    user_prompt = sent_messages[0]["content"]
    
    assert "Tax is 5000" in user_prompt
    assert "[Page 1]" in user_prompt