from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.cookbook import CookbookSchema
from utils.logger import logger

router = APIRouter()


@router.get("/cookbooks/{cookbook_id}", response_model=CookbookSchema)
async def get_cookbook(cookbook_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    cookbook = await mongodb.db.get_collection("cookbooks").find_one({"id": cookbook_id})
    if cookbook is None:
        logger.error("Cookbook does not exist")
        raise HTTPException(status_code=404, detail="Cookbook does not exist")

    sanitized_cookbook = CookbookSchema.sanitize(cookbook)
    return CookbookSchema(**sanitized_cookbook)


@router.get("/cookbooks", response_model=List[CookbookSchema])
async def get_cookbooks():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        cookbooks_cursor = mongodb.db.get_collection("cookbooks").find()
        cookbooks_list = []
        async for cookbook in cookbooks_cursor:
            sanitized_cookbook = CookbookSchema.sanitize(cookbook)
            cookbooks_list.append(CookbookSchema(**sanitized_cookbook))

        return cookbooks_list

    except Exception as e:
        logger.error(f"Failed to retrieve cookbooks: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve cookbooks")
