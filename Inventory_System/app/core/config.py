from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
load_dotenv()  # Ensure .env is loaded


class Settings(BaseSettings):
    DATABASE_1_URL :str
    TITLE:str = Field(default="Student API",description="Title of API")
    DESCRIPTION:str = Field(default="Student API to register students",description="Description of API")
    VERSION : str = Field(default="0.0.1",description="Version of the API") 
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

#Instantiate the class settings to create an object
settings = Settings()

print(f"Loaded DATABASE_URL: {settings.DATABASE_1_URL}")