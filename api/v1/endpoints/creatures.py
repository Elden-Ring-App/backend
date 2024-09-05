from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
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

    return CreatureSchema(**creature)


@router.get("/creatures", response_model=Page[CreatureSchema])
async def get_creatures():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        creatures_cursor = mongodb.db.get_collection("creatures")

        return await paginate(creatures_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve creatures: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve creatures")
