import chromadb
from chromadb.config import Settings
from app.core.config import CHROMA_DIR

client = chromadb.Client(
    Settings(persist_directory = str(CHROMA_DIR))
)

collection = client.get_or_create_collection(
    name = "tax_documents"
)