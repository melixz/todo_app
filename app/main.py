from fastapi import FastAPI, HTTPException
from .models import Task
from typing import List

app = FastAPI()

tasks: List[Task] = []


@app.get("/")
def read_root():
    return {"message": "Welcome to the ToDo App!"}


@app.post("/tasks/")
def create_task(task: Task):
    tasks.append(task)
    return task


@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    return tasks


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for task in tasks:
        if task.id == task_id:
            task.title = updated_task.title
            task.description = updated_task.description
            task.completed = updated_task.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return task
    raise HTTPException(status_code=404, detail="Task not found")