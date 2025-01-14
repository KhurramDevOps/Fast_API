from sqlmodel import Field
from typing import Optional

from app.models.common import BaseModel

class Product(BaseModel, table = True):
    __tablename__ = "products"
    sku_number: int
    product_name: str
    product_description: str
    product_category  : Optional[str]
    product_price: float
    product_quantity: int
    status: Optional[str] = Field(default="active")