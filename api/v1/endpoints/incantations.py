from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
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

    return IncantationSchema(**incantation)


@router.get("/incantations", response_model=Page[IncantationSchema])
async def get_incantations():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        incantations_cursor = mongodb.db.get_collection("incantations")

        return await paginate(incantations_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve incantations: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve incantations")
