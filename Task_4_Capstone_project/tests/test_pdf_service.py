import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from app.services.pdf_service import extract_text_from_pdf

# --- TEST 1: Extraction & Chunking Logic ---
@patch("app.services.pdf_service.PdfReader")
def test_extract_text_success(mock_pdf_reader):
    """Test standard extraction on an unlocked PDF."""
    # 1. Setup Mock PDF
    mock_instance = Mock()
    mock_instance.is_encrypted = False
    
    # Create 2 fake pages
    page1 = Mock(); page1.extract_text.return_value = "Page 1 content."
    page2 = Mock(); page2.extract_text.return_value = "Page 2 content."
    mock_instance.pages = [page1, page2]
    
    mock_pdf_reader.return_value = mock_instance

    # 2. Run Function
    chunks = extract_text_from_pdf("dummy.pdf")
    
    # 3. Verify Logic
    assert len(chunks) == 2
    assert chunks[0]["text"] == "Page 1 content."
    assert chunks[0]["page"] == 1
    assert chunks[1]["page"] == 2

# --- TEST 2: Encryption Logic (No Password) ---
@patch("app.services.pdf_service.PdfReader")
def test_encrypted_pdf_needs_password(mock_pdf_reader):
    """Should fail if PDF is locked and we provide no password."""
    mock_instance = Mock()
    mock_instance.is_encrypted = True
    mock_pdf_reader.return_value = mock_instance

    with pytest.raises(HTTPException) as exc:
        extract_text_from_pdf("locked.pdf", password=None)
    
    assert exc.value.status_code == 422
    assert "password protected" in str(exc.value.detail)

# --- TEST 3: Encryption Logic (Wrong Password) ---
@patch("app.services.pdf_service.PdfReader")
def test_encrypted_pdf_wrong_password(mock_pdf_reader):
    """Should fail if decryption returns 0 (failure)."""
    mock_instance = Mock()
    mock_instance.is_encrypted = True
    mock_instance.decrypt.return_value = 0 # 0 means failed
    mock_pdf_reader.return_value = mock_instance

    with pytest.raises(HTTPException) as exc:
        extract_text_from_pdf("locked.pdf", password="wrong_pass")
    
    assert exc.value.status_code == 400
    assert "Incorrect password" in str(exc.value.detail)