from .db import collection
from .embedding import get_embedding


def semantic_search(query: str, k: int = 3):
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    # Generate embedding for query
    query_embedding = get_embedding(query)

    # Query ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents"]
    )

   
    documents = results.get("documents", [])

    if not documents or not documents[0]:
        return []

    # Return only text chunks
    return documents[0]
