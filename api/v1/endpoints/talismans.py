from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.talisman import TalismanSchema
from utils.logger import logger

router = APIRouter()


@router.get("/talismans/{talisman_id}", response_model=TalismanSchema)
async def get_talisman(talisman_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    talisman = await mongodb.db.get_collection("talismans").find_one({"id": talisman_id})
    if talisman is None:
        logger.error("Talisman does not exist")
        raise HTTPException(status_code=404, detail="Talisman does not exist")

    sanitized_talisman = TalismanSchema.sanitize(talisman)
    return TalismanSchema(**sanitized_talisman)


@router.get("/talismans", response_model=List[TalismanSchema])
async def get_talismans():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        talismans_cursor = mongodb.db.get_collection("talismans").find()
        talismans_list = []
        async for talisman in talismans_cursor:
            sanitized_talisman = TalismanSchema.sanitize(talisman)
            talismans_list.append(TalismanSchema(**sanitized_talisman))

        return talismans_list

    except Exception as e:
        logger.error(f"Failed to retrieve talismans: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve talismans")
