from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
from db.mongo import mongodb
from schemas.material import MaterialSchema
from utils.logger import logger

router = APIRouter()


@router.get("/materials/{material_id}", response_model=MaterialSchema)
async def get_material(material_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    material = await mongodb.db.get_collection("materials").find_one({"id": material_id})
    if material is None:
        logger.error("Material does not exist")
        raise HTTPException(status_code=404, detail="Material does not exist")

    return MaterialSchema(**material)


@router.get("/materials", response_model=Page[MaterialSchema])
async def get_materials():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        materials_cursor = mongodb.db.get_collection("materials")

        return await paginate(materials_cursor)

    except Exception as e:
        logger.error(f"Failed to retrieve materials: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve materials")
