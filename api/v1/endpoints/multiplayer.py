from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.multiplayer import MultiplayerSchema
from utils.logger import logger

router = APIRouter()


@router.get("/multiplayer/{multi_id}", response_model=MultiplayerSchema)
async def get_multi(multi_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    multi = await mongodb.db.get_collection("multi").find_one({"id": multi_id})
    if multi is None:
        logger.error("Multiplayer item does not exist")
        raise HTTPException(status_code=404, detail="Multiplayer item does not exist")

    sanitized_multi = MultiplayerSchema.sanitize(multi)
    return MultiplayerSchema(**sanitized_multi)


@router.get("/multiplayer", response_model=List[MultiplayerSchema])
async def get_multi_items():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        multi_cursor = mongodb.db.get_collection("multi").find()
        multi_list = []
        async for multi in multi_cursor:
            sanitized_multi = MultiplayerSchema.sanitize(multi)
            multi_list.append(MultiplayerSchema(**sanitized_multi))

        return multi_list

    except Exception as e:
        logger.error(f"Failed to retrieve multiplayer items: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve multiplayer items")
