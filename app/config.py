import os
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from the project root
load_dotenv(BASE_DIR / ".env")

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Models
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama-3.3-70b-versatile"

# Paths
CHROMA_DB_DIR = BASE_DIR / "app" / "chroma_db"
DATA_DIR = BASE_DIR / "data"

# Retrieval
TOP_K = 3