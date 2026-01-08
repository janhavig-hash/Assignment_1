from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search():
    payload = {
        "query": "vector database",
        "top_k": 2
    }

    response = client.post("/search", json=payload)
    assert response.status_code == 200
    assert "results" in response.json()
