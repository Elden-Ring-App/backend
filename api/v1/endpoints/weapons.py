from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.weapon import WeaponSchema
from utils.logger import logger

router = APIRouter()


@router.get("/weapons/{weapon_id}", response_model=WeaponSchema)
async def get_weapon(weapon_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    weapon = await mongodb.db.get_collection("weapons").find_one({"id": weapon_id})
    if weapon is None:
        logger.error("Weapon does not exist")
        raise HTTPException(status_code=404, detail="Weapon does not exist")

    sanitized_weapon = WeaponSchema.sanitize(weapon)
    return WeaponSchema(**sanitized_weapon)


@router.get("/weapons", response_model=List[WeaponSchema])
async def get_weapons():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        weapons_cursor = mongodb.db.get_collection("weapons").find()
        weapons_list = []
        async for weapon in weapons_cursor:
            sanitized_weapon = WeaponSchema.sanitize(weapon)
            weapons_list.append(WeaponSchema(**sanitized_weapon))

        return weapons_list

    except Exception as e:
        logger.error(f"Failed to retrieve weapons: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve weapons")
