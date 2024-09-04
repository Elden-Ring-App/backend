import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from utils.logger import logger

from pymongo.errors import ServerSelectionTimeoutError

load_dotenv()


class MongoDB:
    client: AsyncIOMotorClient = None
    db = None


mongodb = MongoDB()


async def connect_to_mongo():
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    port = os.getenv("PORT")
    db_name = os.getenv("DB_NAME")
    host = os.getenv("HOST")

    try:
        mongodb.client = AsyncIOMotorClient(f"mongodb://{username}:{password}@{host}:{port}/")
        #mongodb.client = AsyncIOMotorClient(f"mongodb://{username}:{password}@localhost:{port}/") # to test with no Docker
        await mongodb.client.server_info()
        mongodb.db = mongodb.client.get_database(db_name)

        logger.info("Successfully connected to MongoDB")
    except ServerSelectionTimeoutError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise e


async def close_mongo_connection():
    if mongodb.client:
        mongodb.client.close()
        logger.info("Closed MongoDB connection")
