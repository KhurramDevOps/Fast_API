from pydantic_settings import BaseSettings 
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    mongo_uri: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env file


# Create a global settings instance
settings = Settings() 
