from typing import List
from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate

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

    return MultiplayerSchema(**multi)


@router.get("/multiplayer", response_model=Page[MultiplayerSchema])
async def get_multi_items():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        multi_cursor = mongodb.db.get_collection("multi")

        return await paginate(multi_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve multiplayer items: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve multiplayer items")
