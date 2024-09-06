from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
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

    return ArmorSchema(**armor)


@router.get("/armors", response_model=Page[ArmorSchema])
async def get_armors():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        armors_cursor = mongodb.db.get_collection("armors")

        return await paginate(armors_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve armors: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve armors")
