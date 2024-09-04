from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.ashOfWar import AshOfWarSchema  # Import the correct schema
from utils.logger import logger

router = APIRouter()


@router.get("/ashesOfWar/{ash_id}", response_model=AshOfWarSchema)
async def get_ash_of_war(ash_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    ash = await mongodb.db.get_collection("ashesOfWar").find_one({"id": ash_id})
    if ash is None:
        logger.error("Ash of War does not exist")
        raise HTTPException(status_code=404, detail="Ash of War does not exist")

    sanitized_ash = AshOfWarSchema.sanitize(ash)
    return AshOfWarSchema(**sanitized_ash)


@router.get("/ashesOfWar", response_model=List[AshOfWarSchema])
async def get_ashes_of_war():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        ashes_cursor = mongodb.db.get_collection("ashesOfWar").find()
        ashes_list = []
        async for ash in ashes_cursor:
            sanitized_ash = AshOfWarSchema.sanitize(ash)
            ashes_list.append(AshOfWarSchema(**sanitized_ash))

        return ashes_list

    except Exception as e:
        logger.error(f"Failed to retrieve ashes of war: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve ashes of war")
