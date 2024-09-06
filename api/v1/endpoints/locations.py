from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
from db.mongo import mongodb
from schemas.location import LocationSchema
from utils.logger import logger

router = APIRouter()


@router.get("/locations/{location_id}", response_model=LocationSchema)
async def get_location(location_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    location = await mongodb.db.get_collection("locations").find_one({"id": location_id})
    if location is None:
        logger.error("Location does not exist")
        raise HTTPException(status_code=404, detail="Location does not exist")

    return LocationSchema(**location)


@router.get("/locations", response_model=Page[LocationSchema])
async def get_locations():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        locations_cursor = mongodb.db.get_collection("locations")

        return await paginate(locations_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve locations: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve locations")
