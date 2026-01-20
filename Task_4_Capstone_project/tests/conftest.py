import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add the project root to the python path so imports work
sys.path.append(str(Path(__file__).parent.parent))

from app.main import app

@pytest.fixture
def client():
    """Returns a TestClient that can make fake requests to your API"""
    return TestClient(app)

@pytest.fixture(autouse=True)
def mock_settings():
    """
    Automatically mocks the 'settings' object for ALL tests.
    This prevents tests from needing a real .env file.
    """
    with patch("app.core.config.settings") as mock_settings:
        mock_settings.PROJECT_NAME = "Test Tax Assistant"
        mock_settings.API_PREFIX = "/api"
        # Mock paths to prevent real file creation
        mock_settings.UPLOAD_DIR = Path("/tmp/test_uploads")
        mock_settings.CHROMA_DB_DIR = Path("/tmp/test_db")
        # Mock Models
        mock_settings.EMBEDDING_MODEL = "test-model"
        mock_settings.LLM_MODEL = "test-llm"
        # Mock Limits
        mock_settings.MAX_FILE_SIZE_MB = 10
        mock_settings.TOP_K = 2
        
        yield mock_settings