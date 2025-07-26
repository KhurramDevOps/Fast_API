# app/crud.py

from typing import List, Optional
from bson import ObjectId
from .schemas import CardCreate, CardUpdate
from .database import cards_collection

def _doc_to_card(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "description": doc.get("description"),
    }

async def create_card(card_in: CardCreate) -> dict:
    result = await cards_collection.insert_one(card_in.dict())
    doc = await cards_collection.find_one({"_id": result.inserted_id})
    return _doc_to_card(doc)

async def get_card(card_id: str) -> Optional[dict]:
    doc = await cards_collection.find_one({"_id": ObjectId(card_id)})
    return _doc_to_card(doc) if doc else None

async def get_card_by_title(title: str) -> Optional[dict]:
    doc = await cards_collection.find_one({"title": title})
    return _doc_to_card(doc) if doc else None

async def list_cards() -> List[dict]:
    cards = []
    cursor = cards_collection.find({})
    async for doc in cursor:
        cards.append(_doc_to_card(doc))
    return cards

async def update_card(card_id: str, card_in: CardUpdate) -> Optional[dict]:
    data = {k: v for k, v in card_in.dict(exclude_unset=True).items()}
    if not data:
        return await get_card(card_id)
    await cards_collection.update_one(
        {"_id": ObjectId(card_id)},
        {"$set": data}
    )
    return await get_card(card_id)

async def update_card_by_title(title: str, card_in: CardUpdate) -> Optional[dict]:
    data = {k: v for k, v in card_in.dict(exclude_unset=True).items()}
    if not data:
        return await get_card_by_title(title)
    await cards_collection.update_one(
        {"title": title},
        {"$set": data}
    )
    return await get_card_by_title(title)

async def delete_card(card_id: str) -> bool:
    result = await cards_collection.delete_one({"_id": ObjectId(card_id)})
    return result.deleted_count == 1
