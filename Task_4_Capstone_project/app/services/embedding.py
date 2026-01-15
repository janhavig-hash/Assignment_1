import logging
import ollama
from fastapi import HTTPException, status

EMBED_MODEL = "nomic-embed-text"
MAX_TEXT_LENGTH = 4000 

logger = logging.getLogger(__name__)

def _clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    if len(text) > MAX_TEXT_LENGTH:
        text = text[:MAX_TEXT_LENGTH]
    return text

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for multiple texts (safe, validated, logged)
    Adds 'search_document: ' prefix for Nomic.
    """
    embeddings = []

    if not texts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No text provided for embedding"
        )

    for idx, text in enumerate(texts):
        clean_text = _clean_text(text)

        if not clean_text:
            logger.warning(f"Skipping empty text at index {idx}")
            continue

        try:
            # --- FIX: Add specific prefix for Documents ---
            # This tells the model: "Store this as a retrieval target"
            prompt_text = f"search_document: {clean_text}"

            response = ollama.embeddings(
                model=EMBED_MODEL,
                prompt=prompt_text
            )

            embedding = response.get("embedding")
            if not embedding:
                raise ValueError("Empty embedding returned")

            embeddings.append(embedding)

        except Exception as e:
            logger.exception(f"Embedding failed at index {idx}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Embedding generation failed: {str(e)}"
            )

    if not embeddings:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No valid embeddings could be generated"
        )

    logger.info(f"Generated {len(embeddings)} embeddings")
    return embeddings


def embed_query(text: str) -> list[float]:
    """
    Generate embedding for a single query (safe)
    Adds 'search_query: ' prefix for Nomic.
    """
    clean_text = _clean_text(text)

    if not clean_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query text is empty"
        )

    try:
        # --- FIX: Add specific prefix for Questions ---
        # This tells the model: "Align this with the document vector space"
        prompt_text = f"search_query: {clean_text}"

        response = ollama.embeddings(
            model=EMBED_MODEL,
            prompt=prompt_text
        )

        embedding = response.get("embedding")
        if not embedding:
            raise ValueError("Empty embedding returned")

        return embedding

    except Exception as e:
        logger.exception("Query embedding failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query embedding failed: {str(e)}"
        )