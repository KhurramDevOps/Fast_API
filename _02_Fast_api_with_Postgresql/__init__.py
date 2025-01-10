from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from _02_Fast_api_with_Postgresql.db import init_db, db_session
from _02_Fast_api_with_Postgresql.models import Student
from _02_Fast_api_with_Postgresql.config import settings
from sqlalchemy.exc import IntegrityError
from starlette.middleware.cors import CORSMiddleware

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

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan
)

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def main_root():
    return {"message": "The API is up and running"}

@app.get("/test-db")
async def test_db(session: Session = Depends(db_session)):
    print(session)
    return {"message": "Database is connected"}

@app.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(student_data: Student, session: Session = Depends(db_session)):
    try:
        data = student_data
        statement = select(Student).where(Student.email == data.email)
        isEmailAlreadyExist = session.exec(statement)

        if isEmailAlreadyExist:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

        session.add(data)
        session.commit()
        session.refresh(data)

        return {"status": True, "message": "Student created successfully", "student_data": data}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/students", status_code=status.HTTP_200_OK)
async def get_all_students(session: Session = Depends(db_session)):
    students = session.exec(select(Student)).all()

    if not students:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Students Not found")
    
    return {"status": True, "message": "Students fetched successfully", "student_data": students}

@app.put("/students/{student_id}", status_code=status.HTTP_200_OK)
async def update_single_student(student_id: str, student_data: Student, session: Session = Depends(db_session)):
    statement = select(Student).where(Student.student_id == student_id)
    student = session.exec(statement).first()

    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student Not found")

    student.first_name = student_data.first_name or student.first_name
    student.last_name = student_data.last_name or student.last_name
    student.father_name = student_data.father_name or student.father_name
    student.email = student_data.email or student.email
    student.phone = student_data.phone or student.phone
    student.grade = student_data.grade or student.grade
    student.date_of_birth = student_data.date_of_birth or student.date_of_birth
    student.gender = student_data.gender or student.gender

    try:
        session.add(student)
        session.commit()
        session.refresh(student)
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred.")

    return {"status": True, "message": "Student updated successfully", "student_data": student}

@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK)
async def delete_student(student_id: int, session: Session = Depends(db_session)):
    statement = select(Student).where(Student.student_id == student_id)
    student = session.exec(statement).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student Not found")
    
    session.delete(student)
    session.commit()

    return {"status": True, "message": "Student deleted successfully", "student_id": student.student_id}
