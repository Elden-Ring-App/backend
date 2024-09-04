from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.shieldUpgrade import ShieldUpgradeSchema
from utils.logger import logger

router = APIRouter()


@router.get("/shieldUpgrades/{upgrade_id}", response_model=ShieldUpgradeSchema)
async def get_shield_upgrade(upgrade_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    shield_upgrade = await mongodb.db.get_collection("shieldUpgrades").find_one({"id": upgrade_id})
    if shield_upgrade is None:
        logger.error("Shield Upgrade does not exist")
        raise HTTPException(status_code=404, detail="Shield Upgrade does not exist")

    sanitized_upgrade = ShieldUpgradeSchema.sanitize(shield_upgrade)
    return ShieldUpgradeSchema(**sanitized_upgrade)


@router.get("/shieldUpgrades", response_model=List[ShieldUpgradeSchema])
async def get_shield_upgrades():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        upgrades_cursor = mongodb.db.get_collection("shieldUpgrades").find()
        upgrades_list = []
        async for upgrade in upgrades_cursor:
            sanitized_upgrade = ShieldUpgradeSchema.sanitize(upgrade)
            upgrades_list.append(ShieldUpgradeSchema(**sanitized_upgrade))

        return upgrades_list

    except Exception as e:
        logger.error(f"Failed to retrieve shield upgrades: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve shield upgrades")
