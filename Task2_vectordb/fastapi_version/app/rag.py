import chromadb
import ollama
import numpy as np
from app.config import EMBED_MODEL, COLLECTION_NAME



DOCUMENT_LINES = [
    "Retrieval-Augmented Generation (RAG) is the process of optimizing the output of a large language model, so it references an authoritative knowledge base outside of its training data sources before generating a response.",

    "Large Language Models (LLMs) are trained on vast volumes of data and use billions of parameters to generate original output for tasks like answering questions, translating languages, and completing sentences.",

    "RAG extends the already powerful capabilities of LLMs to specific domains or an organization's internal knowledge base, all without the need to retrain the model.",

    "It is a cost-effective approach to improving LLM output so it remains relevant, accurate, and useful in various contexts."
]




client = chromadb.Client()


try:
    client.delete_collection(COLLECTION_NAME)
except:
    pass

collection = client.create_collection(name=COLLECTION_NAME)


# EMBEDDING FUNCTION 

def create_embedding(text: str):
    response = ollama.embeddings(
        model=EMBED_MODEL,
        prompt=text
    )
    return np.array(response["embedding"])


# STORE DOCUMENT 

def store_document():
    embeddings = []
    ids = []

    for index, line in enumerate(DOCUMENT_LINES):
        embedding = create_embedding(line)
        embeddings.append(embedding.tolist())
        ids.append(f"line_{index}")

    collection.add(
        documents=DOCUMENT_LINES,
        embeddings=embeddings,
        ids=ids
    )

    print(" All document lines embedded and stored successfully")


#  COSINE SIMILARITY 

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# SEARCH 

def search(query: str):
    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=1,
        include=["documents", "embeddings"]
    )

    document = results["documents"][0][0]
    document_embedding = np.array(results["embeddings"][0][0])

    similarity = cosine_similarity(query_embedding, document_embedding)

    return {
        "query": query,
        "matched_document": document,
        "similarity": float(similarity),
        "query_embedding_preview": query_embedding[:10].tolist(),
        "document_embedding_preview": document_embedding[:10].tolist()
    }
