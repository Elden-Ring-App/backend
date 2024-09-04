from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.bell import BellSchema
from utils.logger import logger

router = APIRouter()


@router.get("/bells/{bell_id}", response_model=BellSchema)
async def get_bell(bell_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    bell = await mongodb.db.get_collection("bells").find_one({"id": bell_id})
    if bell is None:
        logger.error("Bell does not exist")
        raise HTTPException(status_code=404, detail="Bell does not exist")

    sanitized_bell = BellSchema.sanitize(bell)
    return BellSchema(**sanitized_bell)


@router.get("/bells", response_model=List[BellSchema])
async def get_bells():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        bells_cursor = mongodb.db.get_collection("bells").find()
        bells_list = []
        async for bell in bells_cursor:
            sanitized_bell = BellSchema.sanitize(bell)
            bells_list.append(BellSchema(**sanitized_bell))

        return bells_list

    except Exception as e:
        logger.error(f"Failed to retrieve bells: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve bells")
