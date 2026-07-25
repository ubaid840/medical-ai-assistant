import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env (for local development)
load_dotenv(BASE_DIR / ".env")

# Try to get API Key from Streamlit Secrets first, then local env
try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found! Please add it to Streamlit Secrets (Settings -> Secrets).")

# Models
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.1-8b-instant"

# Paths
CHROMA_DB_DIR = BASE_DIR / "chroma_db"
DATA_DIR = BASE_DIR / "data"

# Retrieval
TOP_K = 3