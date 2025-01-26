from fastapi import APIRouter, Depends, HTTPException , Header , status
from sqlmodel import Session
from app.core.db import db_session
from app.models.products import Product
from app.api.utils.user_auth_utils import get_user_auth

product_router = APIRouter(prefix="/products",tags=["products"])

@product_router.post("/")
async def create_new_product(product_data: Product, authorization:str = Header(...), session:Session= Depends(get_user_auth)):


    if not authorization.startswith("Bearer"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized to create new product")
    
    token = authorization.split(" ")[1]

    isTokenVerified = session.verify_token(token)
    print(isTokenVerified)
    if not isTokenVerified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"{isTokenVerified}")
    
    
    pass