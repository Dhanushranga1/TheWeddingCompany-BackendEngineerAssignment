📌 Phase 1 — Project Setup + Basic Folder Structure

This phase sets up only the bare minimum structure and the main.py file.

✅ 1. Folder Structure to Create
app/
    main.py
    config.py
    db.py
    routers/
    models/
    schemas/
    utils/

✅ 2. requirements.txt

Create a file:

fastapi
uvicorn
motor
python-jose
passlib[bcrypt]
python-dotenv

✅ 3. config.py

A simple config loader using environment variables.

import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "master_db")
JWT_SECRET = os.getenv("JWT_SECRET", "secret123")
JWT_ALGO = "HS256"

✅ 4. db.py

This connects to MongoDB and exposes the master collections.

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URL, DB_NAME

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

organizations = db["organizations"]
admins = db["admins"]

def get_dynamic_collection(name: str):
    return db[name]

✅ 5. main.py

Basic FastAPI app startup.

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Organization Service Running"}

📌 Expected Git Commit After Phase 1

Your commit message should look like a real junior dev:

init project structure and basic setup