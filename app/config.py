import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "master_db")
JWT_SECRET = os.getenv("JWT_SECRET", "secret123")
JWT_ALGO = "HS256"
