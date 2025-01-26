
from sqlmodel import Field, Relationship
from typing import List, Optional

from app.models.common import BaseModel
from Inventory_System.app.models.product import Product

class User(BaseModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    user_name: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password: str

    # Relationship to products
    products: List["Product"] = Relationship(back_populates="user")