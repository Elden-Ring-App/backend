from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.skill import SkillSchema
from utils.logger import logger

router = APIRouter()


@router.get("/skills/{skill_id}", response_model=SkillSchema)
async def get_skill(skill_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    skill = await mongodb.db.get_collection("skills").find_one({"id": skill_id})
    if skill is None:
        logger.error("Skill does not exist")
        raise HTTPException(status_code=404, detail="Skill does not exist")

    sanitized_skill = SkillSchema.sanitize(skill)
    return SkillSchema(**sanitized_skill)


@router.get("/skills", response_model=List[SkillSchema])
async def get_skills():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        skills_cursor = mongodb.db.get_collection("skills").find()
        skills_list = []
        async for skill in skills_cursor:
            sanitized_skill = SkillSchema.sanitize(skill)
            skills_list.append(SkillSchema(**sanitized_skill))

        return skills_list

    except Exception as e:
        logger.error(f"Failed to retrieve skills: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve skills")
