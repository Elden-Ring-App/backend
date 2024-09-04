from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.sorcery import SorcerySchema
from utils.logger import logger

router = APIRouter()


@router.get("/sorceries/{sorcery_id}", response_model=SorcerySchema)
async def get_sorcery(sorcery_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    sorcery = await mongodb.db.get_collection("sorceries").find_one({"id": sorcery_id})
    if sorcery is None:
        logger.error("Sorcery does not exist")
        raise HTTPException(status_code=404, detail="Sorcery does not exist")

    sanitized_sorcery = SorcerySchema.sanitize(sorcery)
    return SorcerySchema(**sanitized_sorcery)


@router.get("/sorceries", response_model=List[SorcerySchema])
async def get_sorceries():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        sorceries_cursor = mongodb.db.get_collection("sorceries").find()
        sorceries_list = []
        async for sorcery in sorceries_cursor:
            sanitized_sorcery = SorcerySchema.sanitize(sorcery)
            sorceries_list.append(SorcerySchema(**sanitized_sorcery))

        return sorceries_list

    except Exception as e:
        logger.error(f"Failed to retrieve sorceries: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve sorceries")
