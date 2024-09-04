from typing import List
from fastapi import APIRouter, HTTPException
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

    sanitized_material = MaterialSchema.sanitize(material)
    return MaterialSchema(**sanitized_material)


@router.get("/materials", response_model=List[MaterialSchema])
async def get_materials():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        materials_cursor = mongodb.db.get_collection("materials").find()
        materials_list = []
        async for material in materials_cursor:
            sanitized_material = MaterialSchema.sanitize(material)
            materials_list.append(MaterialSchema(**sanitized_material))

        return materials_list

    except Exception as e:
        logger.error(f"Failed to retrieve materials: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve materials")
