from pathlib import Path
import chromadb
import uuid
import logging
from fastapi import HTTPException, status


VECTOR_DB_DIR = Path("data/vector_db")

logger = logging.getLogger(__name__)


client = chromadb.PersistentClient(
    path=str(VECTOR_DB_DIR)
)


collection = client.get_or_create_collection(
    name="tax_documents"
)


def store_chunks(chunks: list[dict], embeddings: list[list[float]]):
    """
    Store text chunks and their embeddings in ChromaDB safely
    """

    if not chunks or not embeddings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chunks or embeddings are empty"
        )

    if len(chunks) != len(embeddings):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Mismatch between chunks and embeddings count"
        )

    ids = []
    documents = []
    metadatas = []

    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        text = chunk.get("text", "").strip()

        if not text:
            logger.warning(f"Skipping empty chunk at index {idx}")
            continue

        ids.append(str(uuid.uuid4()))
        documents.append(text)
        metadatas.append({
            "page": chunk.get("page"),
            "source": chunk.get("source", "uploaded_pdf")
        })

    if not documents:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No valid chunks to store"
        )

    try:
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings[:len(documents)],
            metadatas=metadatas
        )
    except Exception as e:
        logger.exception("Failed to store chunks in ChromaDB")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vector store failed: {str(e)}"
        )

    logger.info(f"Stored {len(documents)} chunks in vector database")


def search_similar(query_embedding: list[float], top_k: int):
    """
    Search for similar documents using vector similarity
    """

    if not query_embedding:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query embedding is empty"
        )

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k * 3
        )
    except Exception as e:
        logger.exception("Vector search failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vector search failed: {str(e)}"
        )

    if not results or not results.get("documents"):
        logger.warning("No matching documents found")

    return results
