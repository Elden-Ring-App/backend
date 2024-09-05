from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
from db.mongo import mongodb
from schemas.keyItem import KeyItemSchema
from utils.logger import logger

router = APIRouter()


@router.get("/keyItems/{key_item_id}", response_model=KeyItemSchema)
async def get_key_item(key_item_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    key_item = await mongodb.db.get_collection("keyItems").find_one({"id": key_item_id})
    if key_item is None:
        logger.error("Key Item does not exist")
        raise HTTPException(status_code=404, detail="Key Item does not exist")

    return KeyItemSchema(**key_item)


@router.get("/keyItems", response_model=Page[KeyItemSchema])
async def get_key_items():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        key_items_cursor = mongodb.db.get_collection("keyItems")

        return await paginate(key_items_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve key items: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve key items")
