# app/main.py

import logging
from fastapi import FastAPI, HTTPException
from typing import List
from . import crud, schemas
from .database import client  # your Motor client

app = FastAPI()

# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Startup event: test Mongo connection
@app.on_event("startup")
async def startup_db_client():
    try:
        # ping the server
        await client.admin.command("ping")
        logger.info("✅ Successfully connected to MongoDB")
    except Exception as e:
        logger.exception("❌ Could not connect to MongoDB")

# Shutdown event: close client
@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    logger.info("🔌 MongoDB connection closed")


@app.post("/cards/", response_model=schemas.Card)
async def create_card(card_in: schemas.CardCreate):
    logger.info(f"→ create_card called: {card_in}")
    return await crud.create_card(card_in)

@app.get("/cards/", response_model=List[schemas.Card])
async def list_cards():
    logger.info("→ list_cards called")
    return await crud.list_cards()

@app.get("/cards/{id}", response_model=schemas.Card)
async def get_card(id: str):
    logger.info(f"→ get_card called: id={id}")
    card = await crud.get_card(id)
    if not card:
        logger.warning(f"⚠️  Card not found: id={id}")
        raise HTTPException(404, "Card not found")
    return card

@app.patch("/cards/{id}", response_model=schemas.Card)
async def update_card(id: str, card_in: schemas.CardUpdate):
    logger.info(f"→ update_card called: id={id}, data={card_in}")
    card = await crud.update_card(id, card_in)
    if not card:
        logger.warning(f"⚠️  Card not found during update: id={id}")
        raise HTTPException(404, "Card not found")
    return card

@app.delete("/cards/{id}")
async def delete_card(id: str):
    logger.info(f"→ delete_card called: id={id}")
    success = await crud.delete_card(id)
    if not success:
        logger.warning(f"⚠️  Card not found during delete: id={id}")
        raise HTTPException(404, "Card not found")
    return {"ok": True}
