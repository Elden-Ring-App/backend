from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
from db.mongo import mongodb
from schemas.npc import NPCSchema
from utils.logger import logger

router = APIRouter()


@router.get("/npcs/{npc_id}", response_model=NPCSchema)
async def get_npc(npc_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    npc = await mongodb.db.get_collection("npcs").find_one({"id": npc_id})
    if npc is None:
        logger.error("NPC does not exist")
        raise HTTPException(status_code=404, detail="NPC does not exist")

    return NPCSchema(**npc)


@router.get("/npcs", response_model=Page[NPCSchema])
async def get_npcs():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        npcs_cursor = mongodb.db.get_collection("npcs")

        return await paginate(npcs_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve NPCs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve NPCs")
