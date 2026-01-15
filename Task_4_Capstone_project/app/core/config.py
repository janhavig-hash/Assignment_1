from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

#Data directories
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
CHROMA_DIR = DATA_DIR / "chroma"

MAX_FILE_SIZE_MB = 20

# App settings
APP_NAME = "AI Personal Tax Assistant"
APP_VERSION = "0.1.0"

# Chunking config
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Retrieval config
TOP_K = 3