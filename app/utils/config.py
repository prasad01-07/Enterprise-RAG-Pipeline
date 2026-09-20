import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Enterprise RAG Pipeline"

DOCUMENTS_DIR = "data/documents"
CHROMA_DB_DIR = "data/chroma_db"

LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)