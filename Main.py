from fastapi import FastAPI # Here this is importing FastAPI which is used to build the API
app = FastAPI() # This creates an instance of the FastAPI app
from pydantic import BaseModel # This imports BaseModel from Pydantic, the BaseModel defines the shape of the data that comes into the API being created
from typing import Optional # This will mark the fields as optional when the data models get defined

# I have created a user class that inherits the BaseModel, this model will define that a user will need to provide a username and password which are both set as strings. The FastAPI will then use this to confirm the incoming requests
class User(BaseModel):
  username: str
  password: str

# Here I defined another class and set what each task has
class Task(BaseModel):
  id: int
  title: str
  description: Optional[str] = None
  completed: bool = False

# This creates an empty dictionary to store the users information in memory
users_db = {}

# This creates an empty list to hold tasks, each task will be a dictionary or a model instance
tasks_db = []

# This allows the user to create a login and it checks if the username is already taken and saves it if it does not. If the username does already exist, it tells them to choose a different one. After signing up it confirms this with the user.
from fastapi import HTTPException

@app.post("/register")
def register(user: User):
  if user.username in users_db:
    raise HTTPException(status_code=400, detail="Username already exists. Please choose a different one")
  users_db[user.username] = user.password
  return {"message": "User registered successfully"}
