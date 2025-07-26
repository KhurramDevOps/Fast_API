from pydantic import BaseModel
from typing import Optional

class CardBase(BaseModel):
    title: str
    description: Optional[str] = None

class CardCreate(CardBase):
    pass

class CardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class Card(CardBase):
    id: str
    class Config:

        from_attributes = True     # for Pydantic v2 (or remove if unused)
        # no need for orm_mode with pure dict responses



