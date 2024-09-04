from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.armor import ArmorSchema
from utils.logger import logger

router = APIRouter()


@router.get("/armors/{armor_id}", response_model=ArmorSchema)
async def get_armors(armor_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    armor = await mongodb.db.get_collection("armors").find_one({"id": armor_id})
    if armor is None:
        logger.error("Armor does not exist")
        raise HTTPException(status_code=404, detail="Armor does not exist")

    sanitized_armor = ArmorSchema.sanitize(armor)
    return ArmorSchema(**sanitized_armor)


@router.get("/armors", response_model=List[ArmorSchema])
async def get_armors():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        armors_cursor = mongodb.db.get_collection("armors").find()
        armors_list = []
        async for armor in armors_cursor:
            sanitized_armor = ArmorSchema.sanitize(armor)
            armors_list.append(ArmorSchema(**sanitized_armor))

        return armors_list

    except Exception as e:
        logger.error(f"Failed to retrieve armors: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve armors")
