from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
from db.mongo import mongodb
from schemas.remembrance import RemembranceSchema
from utils.logger import logger

router = APIRouter()


@router.get("/remembrances/{remembrance_id}", response_model=RemembranceSchema)
async def get_remembrance(remembrance_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    remembrance = await mongodb.db.get_collection("remembrances").find_one({"id": remembrance_id})
    if remembrance is None:
        logger.error("Remembrance does not exist")
        raise HTTPException(status_code=404, detail="Remembrance does not exist")

    return RemembranceSchema(**remembrance)


@router.get("/remembrances", response_model=Page[RemembranceSchema])
async def get_remembrances():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        remembrances_cursor = mongodb.db.get_collection("remembrances")

        return await paginate(remembrances_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve remembrances: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve remembrances")
