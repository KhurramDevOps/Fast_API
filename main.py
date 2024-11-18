from fastapi import FastAPI

app = FastAPI()

# commands to run code
# uvicorn main:app --reload: to reload the server if any change is made
# uvicorn main:app --host 0.0.0.0 --port 800: to run the server on a different host and port
# uvicorn main:app --port=3000or any other port: to run the server on a different port
# curl http://127.0.0.1:8000/docs: to get the swagger
# curl http://127.0.0.1:8000/docs/json: to get the swagger in json format
# curl http://127.0.0.1:8000/items/5: to get the item with id 5


@app.get("/", description="This is our first route. ")
async def root():
    return {"message": "Hello, World"}

@app.post("/")
async def post():
    return {"message": "Hello, from the post route."}

@app.put("/")
async def put():
    return {"message" : "Hello, from the put route."}


# 🔹 GET Method:
# Retrieve data from the server with a simple GET request! Whether you’re fetching user details or items, this method allows us to access information easily.
# GET /users/{me} – Get the details of a specific user.

# 🔹 POST Method:
# Submit data to the server for creating new resources. It’s a great way to send data for creating users, adding items, and more.
# POST / – Simple message to greet from the post route.

# 🔹 PUT Method:
# Want to update an existing resource? The PUT method allows us to modify data on the server. It's all about updating and changing existing information!
# PUT / – Update the resource with a new message.