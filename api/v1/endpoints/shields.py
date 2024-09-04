from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.shield import ShieldSchema
from utils.logger import logger

router = APIRouter()


@router.get("/shields/{shield_id}", response_model=ShieldSchema)
async def get_shield(shield_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    shield = await mongodb.db.get_collection("shields").find_one({"id": shield_id})
    if shield is None:
        logger.error("Shield does not exist")
        raise HTTPException(status_code=404, detail="Shield does not exist")

    sanitized_shield = ShieldSchema.sanitize(shield)
    return ShieldSchema(**sanitized_shield)


@router.get("/shields", response_model=List[ShieldSchema])
async def get_shields():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        shields_cursor = mongodb.db.get_collection("shields").find()
        shields_list = []
        async for shield in shields_cursor:
            sanitized_shield = ShieldSchema.sanitize(shield)
            shields_list.append(ShieldSchema(**sanitized_shield))

        return shields_list

    except Exception as e:
        logger.error(f"Failed to retrieve shields: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve shields")
