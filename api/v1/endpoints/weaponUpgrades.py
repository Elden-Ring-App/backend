from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
from db.mongo import mongodb
from schemas.weaponUpgrade import WeaponUpgradeSchema
from utils.logger import logger

router = APIRouter()


@router.get("/weaponUpgrades/{upgrade_id}", response_model=WeaponUpgradeSchema)
async def get_weapon_upgrade(upgrade_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    weapon_upgrade = await mongodb.db.get_collection("weaponUpgrades").find_one({"id": upgrade_id})
    if weapon_upgrade is None:
        logger.error("Weapon Upgrade does not exist")
        raise HTTPException(status_code=404, detail="Weapon Upgrade does not exist")

    return WeaponUpgradeSchema(**weapon_upgrade)


@router.get("/weaponUpgrades", response_model=Page[WeaponUpgradeSchema])
async def get_weapon_upgrades():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        upgrades_cursor = mongodb.db.get_collection("weaponUpgrades")

        return await paginate(upgrades_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve weapon upgrades: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve weapon upgrades")
