from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from typing import Union

class Priority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class Status(str, Enum):
    COMPLETE = "Completed"
    IN_PROGRESS = "In progress"
    NOT_STARTED = "Not started"
    REJECTED = "Rejected"

app = FastAPI()

class Task(BaseModel):
    task_id : int
    description: str
    status : Status
    priority: Priority

db : list[Task] = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/tasks/all")
async def read_all_tasks():
    return db

@app.get("/tasks/{task_id}")
async def read_task(task_id : int):
    for task in db:
        if task.task_id == task_id:
            return task
    return {"error": "Task not found"}

@app.put("/tasks/new_task")
async def create_task(priority : Priority = Priority.LOW,  
                      description : Union[str | None] = "Default description",
                      status : Status = Status.NOT_STARTED):
    task_id = len(db) + 1

    db.append(Task(task_id=task_id,
                   description=description,
                   status=status,
                   priority=priority))
    
    return {"new task created"}
