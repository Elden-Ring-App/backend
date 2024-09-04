from typing import List
from fastapi import APIRouter, HTTPException
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

    sanitized_location = LocationSchema.sanitize(location)
    return LocationSchema(**sanitized_location)


@router.get("/locations", response_model=List[LocationSchema])
async def get_locations():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        locations_cursor = mongodb.db.get_collection("locations").find()
        locations_list = []
        async for location in locations_cursor:
            sanitized_location = LocationSchema.sanitize(location)
            locations_list.append(LocationSchema(**sanitized_location))

        return locations_list

    except Exception as e:
        logger.error(f"Failed to retrieve locations: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve locations")
