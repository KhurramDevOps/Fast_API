from fastapi import APIRouter, Depends , Header
from sqlmodel import Session
from app.core.db import db_session
from app.models.products import Product
from app.api.utils.user_auth_utils import get_user_auth

product_router = APIRouter(prefix="/products",tags=["products"])

@product_router.post("/")
async def create_new_product(product_data: Product, authorization:str = Header(...), session:Session= Depends(get_user_auth)):

    
    
    
    
    pass