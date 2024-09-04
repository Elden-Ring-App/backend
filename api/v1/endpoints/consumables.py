from typing import List
from fastapi import APIRouter, HTTPException
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

    sanitized_consumable = ConsumableSchema.sanitize(consumable)
    return ConsumableSchema(**sanitized_consumable)


@router.get("/consumables", response_model=List[ConsumableSchema])
async def get_consumables():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        consumables_cursor = mongodb.db.get_collection("consumables").find()
        consumables_list = []
        async for consumable in consumables_cursor:
            sanitized_consumable = ConsumableSchema.sanitize(consumable)
            consumables_list.append(ConsumableSchema(**sanitized_consumable))

        return consumables_list

    except Exception as e:
        logger.error(f"Failed to retrieve consumables: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve consumables")
