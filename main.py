import os

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from db.mongo import connect_to_mongo, close_mongo_connection
from api.v1.endpoints import ammos, armors, bosses, creatures, weapons, ashesOfWar, bells, consumables, cookbooks, \
    crystalTears, greatRunes, incantations, keyItems, locations, materials, multiplayer, NPCs, remembrances, shields, \
    shieldUpgrades, skills, sorceries, spiritAshes, talismans, tools, upgradeMaterials, weaponUpgrades
from dotenv import load_dotenv

app = FastAPI()

if os.getenv("NETLIFY") is None:
    load_dotenv(dotenv_path=".env")

prefix = os.getenv('API_PREFIX')

app.include_router(ammos.router, prefix=f"{prefix}")
app.include_router(armors.router, prefix=f"{prefix}")
app.include_router(bosses.router, prefix=f"{prefix}")
app.include_router(creatures.router, prefix=f"{prefix}")
app.include_router(weapons.router, prefix=f"{prefix}")
app.include_router(ashesOfWar.router, prefix=f"{prefix}")
app.include_router(bells.router, prefix=f"{prefix}")
app.include_router(consumables.router, prefix=f"{prefix}")
app.include_router(cookbooks.router, prefix=f"{prefix}")
app.include_router(crystalTears.router, prefix=f"{prefix}")
app.include_router(greatRunes.router, prefix=f"{prefix}")
app.include_router(incantations.router, prefix=f"{prefix}")
app.include_router(keyItems.router, prefix=f"{prefix}")
app.include_router(locations.router, prefix=f"{prefix}")
app.include_router(materials.router, prefix=f"{prefix}")
app.include_router(multiplayer.router, prefix=f"{prefix}")
app.include_router(NPCs.router, prefix=f"{prefix}")
app.include_router(remembrances.router, prefix=f"{prefix}")
app.include_router(shields.router, prefix=f"{prefix}")
app.include_router(shieldUpgrades.router, prefix=f"{prefix}")
app.include_router(skills.router, prefix=f"{prefix}")
app.include_router(sorceries.router, prefix=f"{prefix}")
app.include_router(spiritAshes.router, prefix=f"{prefix}")
app.include_router(talismans.router, prefix=f"{prefix}")
app.include_router(tools.router, prefix=f"{prefix}")
app.include_router(upgradeMaterials.router, prefix=f"{prefix}")
app.include_router(weaponUpgrades.router, prefix=f"{prefix}")


@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

add_pagination(app)
