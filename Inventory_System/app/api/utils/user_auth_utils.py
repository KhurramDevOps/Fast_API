from fastapi import Depends
import jwt
from sqlmodel import Session , select
from app.core.db import db_session
from typing import Union

from app.models.user import User
import bcrypt
from bcrypt import hashpw
from datetime import datetime, timedelta, timezone

class Auth:
    #constant
    access_token_key = "hd23uodg97ekhbcoue"
    refresh_token_key = "queduegdeuqdh248hdbq"
    def __init__(self, db_session:Session = Depends(db_session)):
        self.db_session = db_session

    async def get_user_by_email(self, email:str) -> Union[User,None]:
        # Transformation of specific data to run validations
        # transformation is type casting , Data operations 
        #khurramshahzad2440@gmail.com
        email_in_lowercase = email.lower()
        statement = select(User).where(User.email == email_in_lowercase)
        # return true or false but it depends on retuning data
        # {id, first_name, last_name, password,email}  
        # True when above data is returned
        # False when no data is returned {}

        user = self.db_session.exec(statement).first()
        # either user will be or not
        return user
    
    
    async def get_user_by_id(self, id:str) -> Union[User,None]:
        user_id = id
        statement = select(User).where(User.email == user_id)
        # return true or false but it depends on retuning data
        # {id, first_name, last_name, password,email}  
        # True when above data is returned
        # False when no data is returned {}

        user = self.db_session.exec(statement).first()
        # either user will be or not
        return user
    
    async def get_user_by_user_name(self, user_name: str) -> Union[User, None]:
            statement = select(User).where(User.user_name == user_name)
            user = self.db_session.exec(statement).first()  #return True or False
            return user

    # Static method
    @staticmethod
    def hash_password(password:str)-> str:
        # use bcrypt to hash password

        salt = bcrypt.gensalt(10)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode("utf-8")

    # static methods are independent of class attributes or methods
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        try:
            if isinstance(hashed_password, str):
                hashed_password = hashed_password.encode("utf-8")
            return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
        except ValueError:
        # Log the error or handle it appropriately
            print("Invalid hashed password format.")
            return False


    
    #Assumptions
    # programmers or developer must write assumptions before writing code
    # create tokens
    # access_token, refresh_token
    # user_id
    #create access_token and refresh_token with JWT
    # expiry date
    # issue date
    # return two things access token and refresh token tuple

    def create_tokens(self, user_id: str)-> tuple[str, str]:
         # issue date 
         issued_at = datetime.now(timezone.utc)
         # expiry date
         access_token_expires_at = datetime.now(timezone.utc) + timedelta(hours = 3)
         refresh_token_expires_at = datetime.now(timezone.utc) + timedelta(days = 7)
         # create access token
         access_token = jwt.encode(
              {"sub": user_id, "exp": access_token_expires_at,"iat":issued_at},
              self.access_token_key,
              algorithm="HS256"
              
         )
         # create refresh token
         refresh_token = jwt.encode(
              {"sub": user_id, "exp": refresh_token_expires_at,"iat":issued_at},
              self.refresh_token_key,
              algorithm="HS256"
              
         )

         return access_token, refresh_token
    
    def verify_tokens(self, token: str, token_type:str= "access"):
        try:
            key = self.create_tokens_key if token_type == "access" else self.refresh_token_key

            verified_token = jwt.decode(token, key, algorithms=["HS256"])

            return verified_token
        except jwt.ExpiredSignatureError:
            print("Your session is expired,  please login again.")
            return None
        except jwt.InvalidTokenError:
            print("Invalid token .")
            return None
        
def get_user_auth(db_session:Session=Depends(db_session))->Auth:
    return Auth(db_session)

         
#userAuth = Auth() #constructor function

# is class is callable/invoke = yes
# object itself is callable/invoke = no
