# db/mongo.py

import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(MONGO_URL)
db = client["product_db"]

# Collections (for reference)
product_collection = db["products"]
orders_collection = db["orders"]
affiliate_links = db["affiliate_links"]
commissions_collection = db["commissions"]
promotion_packages = db["promotion_packages"]



# Local dev settings

# ✅ Directly assign the MongoDB URI for testing
# MONGO_URL = url

# client = AsyncIOMotorClient(MONGO_URL)
# db = client["product_db"]
# product_collection = db["products"]
# orders_collection = db["orders"]
# affiliate_links = db["affiliate_links"]
# commissions_collection = db["commissions"]
# promotion_packages = db["promotion_packages"]
