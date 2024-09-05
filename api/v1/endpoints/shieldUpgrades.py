from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
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

    return ShieldUpgradeSchema(**shield_upgrade)


@router.get("/shieldUpgrades", response_model=Page[ShieldUpgradeSchema])
async def get_shield_upgrades():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        upgrades_cursor = mongodb.db.get_collection("shieldUpgrades")

        return await paginate(upgrades_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve shield upgrades: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve shield upgrades")
