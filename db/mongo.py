import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()


class MongoDB:
    client: AsyncIOMotorClient = None
    db = None


mongodb = MongoDB()


async def connect_to_mongo():
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    port = os.getenv("PORT")
    db_name = os.getenv("B_NAME")
    host = os.getenv("HOST")

    mongodb.client = AsyncIOMotorClient(f"mongodb://{username}:{password}@{host}:{port}/{db_name}")
    mongodb.db = mongodb.client[db_name]


async def close_mongo_connection():
    mongodb.client.close()
