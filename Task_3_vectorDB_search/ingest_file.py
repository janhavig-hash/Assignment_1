import json
from pathlib import Path
from app.db import collection
from app.embedding import get_embedding


DATA_FILE = Path("data/documents.txt")
EXPORT_FILE = Path("data/embeddings.json")


def load_documents():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def ingest_documents():
    documents = load_documents()

    ids = []
    embeddings = []
    export_data = []

    for idx, text in enumerate(documents):
        embedding = get_embedding(text)

        ids.append(str(idx))
        embeddings.append(embedding)

        export_data.append({
            "id": str(idx),
            "text": text,
            "embedding": embedding
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings
    )

    # ✅ Save embeddings to JSON
    with open(EXPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2)

    print(f"Ingested {len(documents)} documents into ChromaDB")
    print(f"Embeddings exported to {EXPORT_FILE}")


if __name__ == "__main__":
    ingest_documents()
