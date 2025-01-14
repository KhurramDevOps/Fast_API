from fastapi import APIRouter, status ,Depends , HTTPException
from app.core.db import db_session
from app.models.users import User
from sqlmodel import Session, select

user_router = APIRouter(prefix="/users",tags=["users"])

@user_router.post("",status_code=status.HTTP_201_CREATED)
async def create_new_users(user_data: User, session:Session = Depends(db_session)):

    if not user_data.first_name  or not user_data.last_name  or not user_data.password or not user_data.email or not user_data.user_name:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Please fill all fields")

    # check if user already exists
    statement = select(User).where(User.user_name == user_data.user_name)
    is_user_name_exist = session.exec(statement).first()  #return True or False
    if is_user_name_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User name already used")
    
    # check if email already exists
    statement = select(User).where(User.email == user_data.email)
    is_email_already_exist = session.exec(statement).first()  #return True or False
    if is_email_already_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already used")  # HTTP_409_CONFLICT Error means that the data already exist

    data= user_data

    try:
        session.add(data)
        session.commit()
        session.refresh(data)
        return {"status":True, "message": "User created successfully", "user": data}
    except Exception as e:
        print(f"error - {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error")



