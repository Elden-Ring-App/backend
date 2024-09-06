from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
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

    return WeaponSchema(**weapon)


@router.get("/weapons", response_model=Page[WeaponSchema])
async def get_weapons():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        weapons_cursor = mongodb.db.get_collection("weapons")

        return await paginate(weapons_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve weapons: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve weapons")
