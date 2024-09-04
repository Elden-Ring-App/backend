from fastapi import FastAPI
from db.mongo import connect_to_mongo, close_mongo_connection, mongodb
from api.v1.endpoints import ammos

app = FastAPI()

app.include_router(ammos.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
