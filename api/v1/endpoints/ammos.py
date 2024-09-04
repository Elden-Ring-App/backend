from typing import List

from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.ammo import AmmoSchema
from utils.logger import logger

router = APIRouter()


@router.get("/ammos/{ammo_id}", response_model=AmmoSchema)
async def get_ammo(ammo_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    ammo = await mongodb.db.get_collection("ammos").find_one({"id": ammo_id})
    if ammo is None:
        logger.error("Ammo does not exist")
        raise HTTPException(status_code=404, detail="Ammo does not exist")

    sanitized_ammo = AmmoSchema.sanitize(ammo)
    return AmmoSchema(**sanitized_ammo)


@router.get("/ammos", response_model=List[AmmoSchema])
async def get_ammos():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        ammos_cursor = mongodb.db.get_collection("ammos").find()
        ammos_list = []
        async for ammo in ammos_cursor:
            sanitized_ammo = AmmoSchema.sanitize(ammo)
            ammos_list.append(AmmoSchema(**sanitized_ammo))

        return ammos_list

    except Exception as e:
        logger.error(f"Failed to retrieve ammos: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve ammos")
