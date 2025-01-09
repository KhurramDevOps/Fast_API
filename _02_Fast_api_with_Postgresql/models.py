 # we need sql model orm to create models for creating database tables
# but we can also create models that we can use to validate/handle request or response


from sqlmodel import SQLModel, Field
import uuid
from datetime import date
from typing import Optional
# we define explicitly that we are going to using this model to create
# table in the data base 

class Student(SQLModel, table=True):
    # entity
    __tablename__ = "Students"
    student_id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name : Optional[str] = None
    last_name : Optional[str]= None
    father_name: Optional[str] =None
    date_of_birth : Optional[date] = None
    gender : Optional[str] = None
    grade: Optional[str] = None
    email:Optional[str] = Field(unique=True,index=True,default=None)
    phone:Optional[str] = None



