from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
from db.mongo import mongodb
from schemas.consumable import ConsumableSchema
from utils.logger import logger

router = APIRouter()


@router.get("/consumables/{consumable_id}", response_model=ConsumableSchema)
async def get_consumable(consumable_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    consumable = await mongodb.db.get_collection("consumables").find_one({"id": consumable_id})
    if consumable is None:
        logger.error("Consumable does not exist")
        raise HTTPException(status_code=404, detail="Consumable does not exist")

    return ConsumableSchema(**consumable)


@router.get("/consumables", response_model=Page[ConsumableSchema])
async def get_consumables():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        consumables_cursor = mongodb.db.get_collection("consumables")

        return await paginate(consumables_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve consumables: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve consumables")
