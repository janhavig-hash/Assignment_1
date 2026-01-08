import chromadb
from chromadb.config import Settings
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


CHROMA_PATH = BASE_DIR / "chroma_db"
CHROMA_PATH.mkdir(exist_ok=True)

client = chromadb.Client(
    Settings(
        persist_directory=str(CHROMA_PATH),
        is_persistent=True,
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection(name="documents")

