from typing import List
from fastapi import APIRouter, HTTPException
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

    sanitized_upgrade = WeaponUpgradeSchema.sanitize(weapon_upgrade)
    return WeaponUpgradeSchema(**sanitized_upgrade)


@router.get("/weaponUpgrades", response_model=List[WeaponUpgradeSchema])
async def get_weapon_upgrades():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        upgrades_cursor = mongodb.db.get_collection("weaponUpgrades").find()
        upgrades_list = []
        async for upgrade in upgrades_cursor:
            sanitized_upgrade = WeaponUpgradeSchema.sanitize(upgrade)
            upgrades_list.append(WeaponUpgradeSchema(**sanitized_upgrade))

        return upgrades_list

    except Exception as e:
        logger.error(f"Failed to retrieve weapon upgrades: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve weapon upgrades")
