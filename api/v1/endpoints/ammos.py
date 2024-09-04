from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from models.ammo import AmmoModel
from utils.logger import logger

router = APIRouter()


@router.get("/ammos/{ammo_id}", response_model=AmmoModel)
async def get_ammo(ammo_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    ammo = await mongodb.db.get_collection("ammos").find_one({"id": ammo_id})
    if ammo is None:
        logger.error("Ammo does not exist")
        raise HTTPException(status_code=404, detail="Ammo does not exist")

    sanitized_ammo = AmmoModel.sanitize(ammo)
    return AmmoModel(**sanitized_ammo)
