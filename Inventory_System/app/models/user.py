
from sqlmodel import Field, Relationship
from typing import Optional, List
from app.models.common import BaseModel
from app.models.product import Product


class User(BaseModel, table=True):
    __tablename__ = "users"
    first_name: str
    last_name: str
    user_name: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password: str
    
    # Relationship to Product
    products: List["Product"] = Relationship(back_populates="user")
