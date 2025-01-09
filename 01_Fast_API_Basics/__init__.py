from fastapi import FastAPI,Query,HTTPException
from typing import Optional,List
from pydantic import BaseModel, field_validator,EmailStr

app = FastAPI(
    title="Dayone of FastAPI",
    description="learning basics of FastAPI",
    version="0.0.1"
)

# first api route

# Get is Http method that is used to getdata from server and send it to the client 
# with get ,  we can use path parameters and query parameters
 
@app.get("/")
async def root():
    return {"status":True,"Message":"API is up"}


class Users(BaseModel):
    user_name: str
    user_email: str
    user_password : str
     
    @field_validator("user_email")
    def validate_email(cls, value):
         if not value.endswith("@example.com"):
             raise ValueError("Email must end with @example.com")
         return value
             

# post is used to create a new resource on the server in the data base
# post request must have body with data
@app.post("/users")
async def create_user(
    user_name: Optional[str] = Query(None),
    user_email:Optional[str] = Query(None),
    user_password: Optional[str] = Query(None)
):
    # data validation

    if user_name is None or user_email is None or user_password is None:
       return {"status":False,"Message":"Please fill all the required fields"}
    
    # Return success Message
    return {"status":True,"Message":"User created successfully"}



@app.post("/users/create")
async def create_user(user_data : Users):
    user = user_data.model_dump()
    print(user)
    return {"status": True, "Message": "User created successfully", "New_user": {"user_name":user["user_name"]}}
    
    

users = [
    {"username": "user1", "email": "john.doe@example.com", "password": "P@ssword123"},
    {"username": "user2", "email": "jane.smith@example.com", "password": "Secure#456"},
    {"username": "user3", "email": "michael.b@example.com", "password": "Michael789!"},
    {"username": "user4", "email": "emily.clark@example.com", "password": "Clark@2024"},
    {"username": "user5", "email": "david.lee@example.com", "password": "Lee*Strong01"},
    {"username": "user6", "email": "sarah.k@example.com", "password": "K!ng$789"},
    {"username": "user7", "email": "robert.j@example.com", "password": "Rob#secure12"},
    {"username": "user8", "email": "olivia.p@example.com", "password": "Pass@Olivia33"},
    {"username": "user9", "email": "daniel.h@example.com", "password": "Hunt3r$2024"},
    {"username": "user10", "email": "mia.walker@example.com", "password": "Walk@r4567"},

]

@app.get("/users")
async def user_data():
    return {"users": users}

@app.get("/users/{user_name}")
async def get_single_user(user_name: str):
    if not user_name:  # Check if the user_name parameter is empty
        return {"message": "User name is required."}
    
    for user in users:
        if user["username"] == user_name:  # Correct the key to match the fake users' dictionary structure
            return {"user": {"user_name":user["username"],"user_email":user["email"]}} # managing the response to not show user password
    
    raise HTTPException(404,"User not found")  # Handle case where user is not found