from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from .models import Task, User
from .utils import find_task, get_password_hash, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

tasks: List[Task] = []
users_db = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.get("/", tags=["Root"], summary="Приветственное сообщение")
def read_root():
    return {"message": "Welcome to the ToDo App!"}


@router.post("/tasks/", response_model=Task, tags=["Tasks"], summary="Создание новой задачи")
def create_task(task: Task):
    tasks.append(task)
    return task


@router.get("/tasks/", response_model=List[Task], tags=["Tasks"], summary="Получение списка всех задач")
def get_tasks():
    return tasks


@router.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"], summary="Обновление задачи по ID")
def update_task(task_id: int, updated_task: Task):
    task = find_task(tasks, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed
    return task


@router.delete("/tasks/{task_id}", response_model=Task, tags=["Tasks"], summary="Удаление задачи по ID")
def delete_task(task_id: int):
    task = find_task(tasks, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks.remove(task)
    return task


@router.post("/register", tags=["Auth"], summary="Регистрация нового пользователя")
def register_user(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    users_db[user.username] = {"username": user.username, "password": hashed_password}
    return {"message": "User registered successfully"}


@router.post("/token", tags=["Auth"], summary="Получение токена доступа")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = user_dict["password"]
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", tags=["Users"], summary="Получение информации о текущем пользователе")
def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
