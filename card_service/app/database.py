# app/database.py

from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

# Create the Motor client
client = AsyncIOMotorClient(settings.mongo_uri)

# Reference your testdb database (from URI)
db = client.get_default_database()      # → this will be “testdb”
cards_collection = db.get_collection("cards")

