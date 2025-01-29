from fastapi import APIRouter, Depends, Header, status, HTTPException
from app.core.db import db_session
from app.models.product import Product
from app.api.utils.user_auth_utils import get_user_auth
from sqlmodel import Session, select
from typing import Optional
from app.api.middlewares.auth_middleware import auth
from app.schemas.product_schema import productSchema
product_router = APIRouter(prefix="/products", tags=["products"])

@product_router.post("/")
async def create_new_product(product_data:productSchema, user_id:str = Depends(auth),db: Session = Depends(db_session)):
    
   

    if not product_data.description or not product_data.price or not product_data.status  or not product_data.product_name or not product_data.product_category or not product_data.quantity:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="All fields are required")
    # Handle the invalid data case
   
    
    # we accept the user_id from auth middleware hwhich is coming after

    # as we are validating our body data on the bais of 
    # schema model whhich is not fro database tables
    # therefore, we need to firt dump the incoming data
    # into python dictionary using model_dump() method
    data = product_data.model_dump()
    data["user_id"] = user_id
    # after that we use main Product mdel to creat edat
    # that we use to save in databse
    # ** mean destructive 
    #
    data = Product(**data)
    db.add(data)
    db.commit()
    db.refresh(data)
        

    
    return {"status":True, "message":"Product is created successfully", "data":product_data}



@product_router.get("/")
async def get_all_products(auth = Depends(auth), db: Session = Depends(db_session)):


    statement = select(Product)
    products =  db.exec(statement).all()

    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product found")

    return {"status":True, "message":"products fetched successfully", "data": products}



# # create endpoint to get signle product
# from fastapi import FastAPI, HTTPException
# from uuid import UUID

# app = FastAPI()

# # Sample product data
# products = {
#     UUID("123e4567-e89b-12d3-a456-426614174000"): {"id": "123e4567-e89b-12d3-a456-426614174000", "name": "Laptop", "price": 1200},
#     UUID("123e4567-e89b-12d3-a456-426614174001"): {"id": "123e4567-e89b-12d3-a456-426614174001", "name": "Phone", "price": 800},
# }

# @app.get("/products/{product_id}")
# def get_product(product_id: UUID):
#     product = products.get(product_id)
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return product


# create endpoint to get products of any single user
    
