import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():

    """
    Create a fastapi test cleint that can send requests to your API 

    """
    return TestClient(app)