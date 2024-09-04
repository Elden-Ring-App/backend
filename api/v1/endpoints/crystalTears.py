from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.crystalTear import CrystalTearSchema
from utils.logger import logger

router = APIRouter()


@router.get("/crystalTears/{tear_id}", response_model=CrystalTearSchema)
async def get_crystal_tear(tear_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    tear = await mongodb.db.get_collection("crystalTears").find_one({"id": tear_id})
    if tear is None:
        logger.error("Crystal Tear does not exist")
        raise HTTPException(status_code=404, detail="Crystal Tear does not exist")

    sanitized_tear = CrystalTearSchema.sanitize(tear)
    return CrystalTearSchema(**sanitized_tear)


@router.get("/crystalTears", response_model=List[CrystalTearSchema])
async def get_crystal_tears():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        tears_cursor = mongodb.db.get_collection("crystalTears").find()
        tears_list = []
        async for tear in tears_cursor:
            sanitized_tear = CrystalTearSchema.sanitize(tear)
            tears_list.append(CrystalTearSchema(**sanitized_tear))

        return tears_list

    except Exception as e:
        logger.error(f"Failed to retrieve crystal tears: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve crystal tears")
