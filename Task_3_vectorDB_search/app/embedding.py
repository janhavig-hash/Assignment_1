import ollama

MODEL_NAME = "nomic-embed-text"

def get_embedding(text: str) -> list:
    if not text.strip():
        raise ValueError("Text cannot be empty")

    response = ollama.embeddings(
        model=MODEL_NAME,
        prompt=text
    )
    return response["embedding"]
