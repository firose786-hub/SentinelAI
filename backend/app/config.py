import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
base_dir = Path(__file__).resolve().parent.parent
load_dotenv(base_dir / ".env")

PORT = int(os.getenv("PORT", "5000"))
HOST = os.getenv("HOST", "0.0.0.0")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

DATABASE_PATH = str(base_dir / "data" / "analyses.db")
Path(base_dir / "data").mkdir(parents=True, exist_ok=True)
