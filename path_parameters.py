from enum import Enum
from fastapi import FastAPI

app =FastAPI()

# PATH PARAMETERS
# Path parameters are dynamic values that are included in the URL of the endpoint.
# They are used to pass data to the API in the URL itself. 
# Path parameters are usually used to identify a specific resource (like an ID or a name).f

@app.get("/",description="This is our main route.")
async def root():
    return {"message":"HELLO WORLD!"}

@app.get("/users")
async def list_items():
    return {"message":"list of several users"}

@app.get("/users/{me}")
async def get_current_user(me : str):
    return {"message": f"This is the current {me}"}

@app.get("/users/{users_id}")
async def get_id(users_id:str):
    return{"user_id": users_id}

class FoodEnum(str , Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"

@app.get("/foods/{food_name}")
async def get_food(food_name : FoodEnum):
    if food_name == FoodEnum.vegetables:
        return{"food_name" : food_name ,"message": "You are healthy"}
    
    if food_name.value == "fruits":
        return {
            "food_name" : food_name, 
                "message" : "you are still healthy, but like sweet things"
                }
    
    return {
        "food_name" : food_name,"message" :"I like chocolate milk"}
    