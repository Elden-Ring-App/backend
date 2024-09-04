from typing import List
from fastapi import APIRouter, HTTPException
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

    sanitized_npc = NPCSchema.sanitize(npc)
    return NPCSchema(**sanitized_npc)


@router.get("/npcs", response_model=List[NPCSchema])
async def get_npcs():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        npcs_cursor = mongodb.db.get_collection("npcs").find()
        npcs_list = []
        async for npc in npcs_cursor:
            sanitized_npc = NPCSchema.sanitize(npc)
            npcs_list.append(NPCSchema(**sanitized_npc))

        return npcs_list

    except Exception as e:
        logger.error(f"Failed to retrieve NPCs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve NPCs")
