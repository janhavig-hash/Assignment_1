import chromadb
from chromadb.config import Settings
from pathlib import Path

# Absolute path to project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Persistent DB folder
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
