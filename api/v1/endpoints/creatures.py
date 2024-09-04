from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.creature import CreatureSchema
from utils.logger import logger

router = APIRouter()


@router.get("/creatures/{creature_id}", response_model=CreatureSchema)
async def get_creature(creature_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    creature = await mongodb.db.get_collection("creatures").find_one({"id": creature_id})
    if creature is None:
        logger.error("Creature does not exist")
        raise HTTPException(status_code=404, detail="Creature does not exist")

    sanitized_creature = CreatureSchema.sanitize(creature)
    return CreatureSchema(**sanitized_creature)


@router.get("/creatures", response_model=List[CreatureSchema])
async def get_creatures():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        creatures_cursor = mongodb.db.get_collection("creatures").find()
        creatures_list = []
        async for creature in creatures_cursor:
            sanitized_creature = CreatureSchema.sanitize(creature)
            creatures_list.append(CreatureSchema(**sanitized_creature))

        return creatures_list

    except Exception as e:
        logger.error(f"Failed to retrieve creatures: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve creatures")
