from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.boss import BossSchema
from utils.logger import logger

router = APIRouter()


@router.get("/bosses/{boss_id}", response_model=BossSchema)
async def get_boss(boss_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    boss = await mongodb.db.get_collection("bosses").find_one({"id": boss_id})
    if boss is None:
        logger.error("Boss does not exist")
        raise HTTPException(status_code=404, detail="Boss does not exist")

    sanitized_boss = BossSchema.sanitize(boss)
    return BossSchema(**sanitized_boss)


@router.get("/bosses", response_model=List[BossSchema])
async def get_bosses():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        bosses_cursor = mongodb.db.get_collection("bosses").find()
        bosses_list = []
        async for boss in bosses_cursor:
            sanitized_boss = BossSchema.sanitize(boss)
            bosses_list.append(BossSchema(**sanitized_boss))

        return bosses_list

    except Exception as e:
        logger.error(f"Failed to retrieve bosses: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve bosses")
