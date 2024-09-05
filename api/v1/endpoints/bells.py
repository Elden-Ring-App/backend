from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
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

    return BellSchema(**bell)


@router.get("/bells", response_model=Page[BellSchema])
async def get_bells():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        bells_cursor = mongodb.db.get_collection("bells")

        return await paginate(bells_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve bells: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve bells")
