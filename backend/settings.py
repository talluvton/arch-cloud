import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "architectures_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "architectures_collection")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")