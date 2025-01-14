from fastapi import FastAPI, HTTPException , status
from contextlib import asynccontextmanager

from app.core.db import initialize_db
from app.core.config import settings
from app.api.main import api_router

@asynccontextmanager
async def life_span(ap:FastAPI):
    print("Lifespan started")
    try:
        initialize_db()
        yield
    except Exception as e:
        print(f"Error in lifespan: {e}")

    print("Lifespan ended")
  
    

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=life_span
)

@app.get("/",status_code=status.HTTP_200_OK)
async def root():
    return {"status": True , "message": "API is up"}

app.include_router(api_router)



