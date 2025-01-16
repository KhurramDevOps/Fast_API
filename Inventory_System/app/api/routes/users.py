from fastapi import APIRouter, Form, Response, status ,Depends , HTTPException
from app.core.db import db_session
from app.models.users import User
from sqlmodel import Session, select
from app.api.utils.user_auth_utils import  Auth

user_router = APIRouter(prefix="/users",tags=["users"])

def get_user_auth(db_session: Session = Depends(db_session)) -> Auth:
    return Auth(db_session)



@user_router.post("/signup",status_code=status.HTTP_201_CREATED)
async def create_new_users(user_data: User, user_Auth:Auth = Depends(get_user_auth)):

    if not user_data.first_name  or not user_data.last_name  or not user_data.password or not user_data.email or not user_data.user_name:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Please fill all fields")

    # check if user already exists
    user_by_user_name = await user_Auth.get_user_by_user_name(user_data.user_name)
    if user_by_user_name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User name already used")
    
    # Email validation through get_user_by_email method
    user =  await user_Auth.get_user_by_email(user_data.email)
    
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already used")  # HTTP_409_CONFLICT Error means that the data already exist
    print(f"user common password is {user_data.password}")
    #Hashed Password
    hashed_password = user_Auth.hash_password(user_data.password)
    user_data.password = hashed_password  # replacing the original user password with hashed password
    
    print(f"user with hashed password is {user_data}")

    data= user_data

    try:
        user_Auth.db_session.add(data)
        user_Auth.db_session.commit()
        user_Auth.db_session.refresh(data)
        return {"status":True, "message": "User created successfully", "user": data}
    except Exception as e:
        print(f"error - {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error")

@user_router.post("/signin") 
async def signin_user(response:Response,user_email: str = Form(...),user_password: str = Form(...),
                       user_Auth:Auth = Depends(get_user_auth)):  #Query parameters, these are shown in URL

    is_user_exist = await user_Auth.get_user_by_email(user_email)

    if not  is_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "user with this email not exist")
    
    is_password_match = user_Auth.verify_password(user_password,is_user_exist.password)
    
    if not is_password_match:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail = "Invalid Credentials")
    
    user_id = str(is_user_exist.id)
    access_token , refresh_token= user_Auth.create_tokens(user_id)
  
    response.set_cookie(
        key="inventory_refresh_token",
        value= refresh_token,
        httponly = False,
        secure = True,
        samesite= "strict"

    )
    return{
        "status":True,
        "message": "you are logged in successfully",
        "access_token":access_token,
        "user": is_user_exist

    }

# path_parameters -> static & dynamic
# query parameters -> that we declare in function as parameter



