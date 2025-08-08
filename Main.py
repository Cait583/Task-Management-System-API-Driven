from fastapi import FastAPI # Here this is importing FastAPI which is used to build the API
app = FastAPI() # This creates an instance of the FastAPI app
from pydantic import BaseModel # This imports BaseModel from Pydantic, the BaseModel defines the shape of the data that comes into the API being created
from typing import Optional # This will mark the fields as optional when the data models get defined

# I have created a user class that inherits the BaseModel
# This model will define that a user will need to provide a username and password which are both set as strings
# The FastAPI will then use this to confirm the incoming requests
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

# This allows the user to create a login and it checks if the username is already taken and saves it if it does not
# If the username does already exist, it tells them to choose a different one
# After signing up it confirms this with the user
from fastapi import HTTPException

@app.post("/register")
def register(user: User):
  if user.username in users_db:
    raise HTTPException(status_code=400, detail="Username already exists. Please choose a different one")
  users_db[user.username] = user.password
  return {"message": "User registered successfully"}

# Here this will let the user login, if the username does not exist or the password is incorrect it shows an error
# If the login works it will confirm with the user telling them it was successful
@app.post("/login")
def login(user: User):
  if user.username not in users_db:
    raise HTTPException(status_code=404, detail="User not found")
  if users_db[user.username] != user.password:
    raise HTTPException(status_code=401, detail="Incorrect password")
  return {"message": "Login successful"}

# This makes a post route at /tasks which is used to create new tasks
# The task then gets added to the tasks_db list
# Adds a new task to the list. It takes the task information and stored it then tells the user task created
@app.post("/tasks")
def create_task(task: Task):
  tasks_db.append(task)
  return {"message": "Task created", "task": task}

# This creates a GET route at /tasks and then when the user visits the route it shows the full list of tasks in tasks.db
@app.get("/tasks")
def get_tasks():
  return tasks_db

# This is a PUT route at /tasks/{task_id} which means update task with this ID
# Then it will loop through the tasks to find one with the matching id
# If it gets found it will replace the old task with the new one that gets created
# If it does not get found the user will see the error message of 404
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
  for index, task in enumerate(tasks_db):
    if task.id == task_id:
      tasks_db[index] = updated_task
      return {"message": "Task updated", "task": updated_task}
  raise HTTPException(status_code=404, detail="Task not found")

# This is a DELETE route located at /tasks/{task_id}
# It will look for the task with that ID
# If it is found then it deletes it from the list
# If it does not then it will return an error message
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
  for index, task in enumerate(tasks_db):
    if task.id == task_id:
      tasks_db.pop(index)
      return {"message": "Task deleted"}
  raise HTTPException(status_code=404, detail="Task not found")
