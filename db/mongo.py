import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URI")  # Reads from environment variable

client = AsyncIOMotorClient(MONGO_URL)
db = client["product_db"]
product_collection = db["products"]
