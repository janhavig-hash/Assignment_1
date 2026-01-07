import os
from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL = os.getenv("EMBED_MODEL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
API_URL = os.getenv("API_URL")

if not EMBED_MODEL or not COLLECTION_NAME:
    raise ValueError("Missing environment variables. Check .env file.")
