import uuid
from sqlmodel import Field, Relationship
from typing import Optional
from uuid import UUID

from app.models.common import BaseModel

class Product(BaseModel, table=True):
    __tablename__ = "products"
    id: Optional[int] = Field(default=None, primary_key=True)
    sku_number: int
    product_name: str
    product_description: str
    product_category: Optional[str]
    product_price: float
    product_quantity: int
    status: Optional[str] = Field(default="active")

    # Foreign key and relationship
    user_id: uuid.UUID = Field(default=None, foreign_key="users.id")
    user: Optional[User] = Relationship(back_populates="products")