from pydantic_settings import BaseSettings 
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    mongo_uri: str 


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create a global settings instance
settings = Settings() 
