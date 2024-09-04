from typing import List
from fastapi import APIRouter, HTTPException
from db.mongo import mongodb
from schemas.tool import ToolSchema
from utils.logger import logger

router = APIRouter()


@router.get("/tools/{tool_id}", response_model=ToolSchema)
async def get_tool(tool_id: int):
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    tool = await mongodb.db.get_collection("tools").find_one({"id": tool_id})
    if tool is None:
        logger.error("Tool does not exist")
        raise HTTPException(status_code=404, detail="Tool does not exist")

    sanitized_tool = ToolSchema.sanitize(tool)
    return ToolSchema(**sanitized_tool)


@router.get("/tools", response_model=List[ToolSchema])
async def get_tools():
    if mongodb.db is None:
        logger.error("Database connection not initialized")
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    try:
        tools_cursor = mongodb.db.get_collection("tools").find()
        tools_list = []
        async for tool in tools_cursor:
            sanitized_tool = ToolSchema.sanitize(tool)
            tools_list.append(ToolSchema(**sanitized_tool))

        return tools_list

    except Exception as e:
        logger.error(f"Failed to retrieve tools: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve tools")
