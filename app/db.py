from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URL, DB_NAME

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

organizations = db["organizations"]
admins = db["admins"]

async def create_indexes():
    await organizations.create_index("name", unique=True)
    await admins.create_index("email", unique=True)

def get_dynamic_collection(name: str):
    return db[name]
