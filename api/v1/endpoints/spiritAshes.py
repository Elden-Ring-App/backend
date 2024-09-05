from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate

from db.mongo import mongodb
from schemas.spiritAsh import SpiritAshSchema
from utils.logger import logger

router = APIRouter()


@router.get("/spiritAshes/{spirit_ash_id}", response_model=SpiritAshSchema)
async def get_spirit_ash(spirit_ash_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    spirit_ash = await mongodb.db.get_collection("spiritAshes").find_one({"id": spirit_ash_id})
    if spirit_ash is None:
        logger.error("Spirit Ash does not exist")
        raise HTTPException(status_code=404, detail="Spirit Ash does not exist")

    return SpiritAshSchema(**spirit_ash)


@router.get("/spiritAshes", response_model=Page[SpiritAshSchema])
async def get_spirit_ashes():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        spirit_ashes_cursor = mongodb.db.get_collection("spiritAshes")

        return await paginate(spirit_ashes_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve spirit ashes: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve spirit ashes")
