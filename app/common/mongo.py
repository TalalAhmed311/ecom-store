from motor.motor_asyncio import AsyncIOMotorClient
from app.common.config import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client.get_database("ecom_mongo")

async def get_mongo():
    return db
