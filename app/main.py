from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import create_tables
from app.task.models import Task
from pydantic import BaseModel
from app.task.services import (
create_task,
update_task,
get_all_tasks,
get_task_by_id,
patch_task,
delete_task
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)

class Task_Cruder(BaseModel):
    title: str
    content: str

@app.post("/task", response_model=Task)
def task_create(new_task: Task_Cruder):
    task = create_task(new_task.title, new_task.content)
    return task

@app.get("/tasks", response_model=list[Task])
def tasks_list():
    tasks = get_all_tasks()
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def task_detail(task_id: int):
    task = get_task_by_id(task_id)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def task_update(task_id: int, new_task: Task_Cruder):
    task = update_task(task_id, new_task.title, new_task.content)
    return task

@app.patch("/tasks/{task_id}", response_model=Task)
def task_partial_update(task_id: int, new_task: Task_Cruder):
    task = patch_task(task_id, new_task)
    return task

@app.delete("/tasks/{task_id}")
def task_delete(task_id: int):
    delete_task(task_id)
    return {"message": "Task deleted"}