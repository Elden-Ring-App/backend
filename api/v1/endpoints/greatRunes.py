from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.greatRune import GreatRuneSchema
from utils.logger import logger

router = APIRouter()

@router.get("/greatRunes/{rune_id}", response_model=GreatRuneSchema)
async def get_great_rune(rune_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    rune = await mongodb.db.get_collection("greatRunes").find_one({"id": rune_id})
    if rune is None:
        logger.error("Great Rune does not exist")
        raise HTTPException(status_code=404, detail="Great Rune does not exist")

    sanitized_rune = GreatRuneSchema.sanitize(rune)
    return GreatRuneSchema(**sanitized_rune)


@router.get("/greatRunes", response_model=List[GreatRuneSchema])
async def get_great_runes():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        runes_cursor = mongodb.db.get_collection("greatRunes").find()
        runes_list = []
        async for rune in runes_cursor:
            sanitized_rune = GreatRuneSchema.sanitize(rune)
            runes_list.append(GreatRuneSchema(**sanitized_rune))

        return runes_list

    except Exception as e:
        logger.error(f"Failed to retrieve great runes: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve great runes")
