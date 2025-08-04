from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://joe:1kotWWXWu0aFznUc@cluster0.agajrkh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # or your MongoDB Atlas URI

client = AsyncIOMotorClient(MONGO_URL)
db = client["product_db"]
product_collection = db["products"]