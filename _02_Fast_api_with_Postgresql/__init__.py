# we import FASTAPI from fastapi
from fastapi import FastAPI , Depends ,HTTPException,status
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from _02_Fast_api_with_Postgresql.db import init_db, db_session
from _02_Fast_api_with_Postgresql.models import Student
from _02_Fast_api_with_Postgresql.config import settings
from sqlalchemy.exc import IntegrityError

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan Start")
    try:
        init_db()
        print("Database initialized and tables are created")
    except Exception as e:
        print(f"Error initializing database: {e}")
    yield
    print("Lifespan End")

# promise
# promise in async programming has three stages
# pending,  resolved , rejected


# Initialize the fastapi instance to create a server
app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan
)

# http methods mostly used
# get, post , put, patch, delete

# Root Get Route to check whether our api is up or down.
@app.get("/")
def main_root():
    return {"message": "The API is up and running"}


@app.get("/test-db")
async def test_db(session:Session = Depends(db_session)):
    print(session)
    return {"message": "Database is connected"}

# create a student post endpoint to create a new student
@app.post("/students",status_code=status.HTTP_201_CREATED)
async def create_student(student_data:Student, session: Session = Depends(db_session)):
    try:
        # Accept data from frontend in function as student_data ,, then assign student_data
        # to data variable
        data = student_data

        statement = select(Student).where(Student.email == data.email)
        isEmailAlreadyExist = session.exec(statement)

        if isEmailAlreadyExist:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        # here , we add our data into session
        session.add(data)
        # commit the data to the database table
        session.commit()
        

        # here we return the created student data from database
        session.refresh(data)
        print(data)


        return {"status":True ,"message": "Student created successfully", "student_data":data}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        

# get all students from database and send t0 the client
@app.get("/students/{student_id}",status_code=status.HTTP_200_OK) #dynamic path parameters
async def get_all_students(student_id : str ,session: Session = Depends(db_session)):

        statement = select(Student).where(Student.student_id == student_id)
        isStudentExist = session.exec(statement).first() #when it finds the id at 55 from total 100 it will reutrn this not to check the 45 more

        if not isStudentExist:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student Not found")
        
        else:
            return {"status":True ,"message": "Students fetched successfully","student_data":isStudentExist}
        
        

# create a put request to update the student data in databae
# fro this purpose we need two types of data
#  1 . student id to check whether the student exsit or not
# 2. data that we want ot change in our data base

@app.put("/students/{student_id}")
async def update_single_student(student_id : str , student_data : Student , session : Session = Depends(db_session)):

    #validate data
    student_id = student_id

    if student_id is None:
        raise HTTPException(status_code=422, detail="Student id is required.")
    statement = select(Student).where(Student.student_id == student_id)
    student = session.exec(statement).first() #when it finds the id at 55 from total 100 it will reutrn this not to check the 45 more

    if  student is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student Not found")
        
    if student:
         student.first_name = student_data.first_name or student.first_name   # here we are handling that in changing when these fields are empty consider the old data and add in db
         student.last_name = student_data.last_name  or student.last_name
         student.father_name = student_data.father_name or student.father_name
         student.email = student_data.email or student.email                     
         student.phone = student_data.phone or student.phone
         student.grade  = student_data.grade or student.grade
         student.date_of_birth = student_data.date_of_birth or student.date_of_birth
         student.gender = student_data.gender or student.gender

    try:   
        session.add(student)
        session.commit()
        session.refresh(student)

    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred.")

    return{"status":True,"message":"student updated successfully","student_data":student}

        
# delete route to delete studetn on the basis of id in the data base
@app.delete("/students/{student_id}")
async def delete_student(student_id : str , session : Session = Depends(db_session)):
     
     if student_id is None:
          raise HTTPException(status_code=422, detail="Student id is required.")
     select_student = select(Student).where(Student.student_id == student_id)
     student = session.exec(select_student).first()
    
     if student:
          session.delete(student)
          session.commit()
          return {"status":True,"message":"student deleted successfully", "student_id":student.student_id}
     else:
          
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student Not found")