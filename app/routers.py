from fastapi import APIRouter, HTTPException
from typing import List
from .models import Task
from .utils import find_task

router = APIRouter()

tasks: List[Task] = []


@router.get("/")
def read_root():
    return {"message": "Welcome to the ToDo App!"}


@router.post("/tasks/", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task


@router.get("/tasks/", response_model=List[Task])
def get_tasks():
    return tasks


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    task = find_task(tasks, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed
    return task


@router.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    task = find_task(tasks, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks.remove(task)
    return task
