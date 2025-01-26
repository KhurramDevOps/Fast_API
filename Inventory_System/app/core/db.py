from typing import Generator
from sqlmodel import create_engine, Session, SQLModel
# from Inventory_System.app.models.user import User
# from Inventory_System.app.models.product import Product
from app.core.config import settings

class Database:
    # create constructor function
    # when class i used , below dunder function will run automatically
    def __init__(self,db_url:str):
        self.db_url = db_url.replace("postgresql","postgresql+psycopg2")
        self.engine = create_engine(self.db_url)

    def initialize_db(self) -> None:
        try:
            print("Start creating database tables: {self.db_url}")
            SQLModel.metadata.create_all(self.engine)
            print("Database tables created successfully")
        except Exception as e:
            print(f"Failed to create database tables: {e}")
            return 
        
    def db_sessions(self) ->Generator[Session,None, None]:
         
        with Session(self.engine) as session:
                try:
                    yield session
                except Exception as e:
                    print(f"Failed to create database session: {e}")
                    raise
                finally:
                    session.close()


db = Database(settings.DATABASE_1_URL)

def initialize_db()->None:
    db.initialize_db()

def db_session()->Generator[Session, None, None]:
    yield from db.db_sessions()  

