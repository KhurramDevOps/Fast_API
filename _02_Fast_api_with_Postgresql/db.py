from sqlmodel import create_engine , Session, SQLModel
from _02_Fast_api_with_Postgresql.models import Student
from typing import Generator
from _02_Fast_api_with_Postgresql.config import settings
from sqlalchemy.ext.asyncio import AsyncEngine

#  database connection string to connect wth db using engine
db_connection_string = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg2")


# Create engine which mange the connection to the data base and its connection pool
engine = create_engine(db_connection_string, pool_recycle=300)


#  function that we use in life span to create tables in the database using models
def init_db()-> None:
    SQLModel.metadata.create_all(engine)

# we use this function as middle layer to  build session fro data transferring with database
def db_session()-> Generator[Session,None, None]:
    with Session(engine) as session:
        yield session  #yield mean return

