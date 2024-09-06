from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
from db.mongo import mongodb
from schemas.upgradeMaterial import UpgradeMaterialSchema
from utils.logger import logger

router = APIRouter()


@router.get("/upgradeMaterials/{material_id}", response_model=UpgradeMaterialSchema)
async def get_upgrade_material(material_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    material = await mongodb.db.get_collection("upgradeMaterials").find_one({"id": material_id})
    if material is None:
        logger.error("Upgrade Material does not exist")
        raise HTTPException(status_code=404, detail="Upgrade Material does not exist")

    return UpgradeMaterialSchema(**material)


@router.get("/upgradeMaterials", response_model=Page[UpgradeMaterialSchema])
async def get_upgrade_materials():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        materials_cursor = mongodb.db.get_collection("upgradeMaterials")

        return await paginate(materials_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve upgrade materials: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve upgrade materials")
