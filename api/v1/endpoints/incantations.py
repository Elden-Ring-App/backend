from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.incantation import IncantationSchema
from utils.logger import logger

router = APIRouter()


@router.get("/incantations/{incantation_id}", response_model=IncantationSchema)
async def get_incantation(incantation_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    incantation = await mongodb.db.get_collection("incantations").find_one({"id": incantation_id})
    if incantation is None:
        logger.error("Incantation does not exist")
        raise HTTPException(status_code=404, detail="Incantation does not exist")

    sanitized_incantation = IncantationSchema.sanitize(incantation)
    return IncantationSchema(**sanitized_incantation)


@router.get("/incantations", response_model=List[IncantationSchema])
async def get_incantations():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        incantations_cursor = mongodb.db.get_collection("incantations").find()
        incantations_list = []
        async for incantation in incantations_cursor:
            sanitized_incantation = IncantationSchema.sanitize(incantation)
            incantations_list.append(IncantationSchema(**sanitized_incantation))

        return incantations_list

    except Exception as e:
        logger.error(f"Failed to retrieve incantations: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve incantations")
