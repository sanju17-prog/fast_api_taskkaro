from sqlmodel import Session, select
from app.task.models import Task
from app.db.config import engine, SessionDep
from fastapi import HTTPException
from pydantic import BaseModel

class TaskCrud(BaseModel):
    title: str
    content: str

def create_task(session: SessionDep, title: str, content: str):
    task = Task(title=title, content=content)
    # with Session(engine) as session:
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_all_tasks(session: SessionDep):
    # with Session(engine) as session:
    stmt = select(Task)
    tasks = session.exec(stmt)
    return tasks.all()

def get_task_by_id(session: SessionDep, task_id: int):
    # with Session(engine) as session:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def update_task(session: SessionDep, task_id: int, title: str, content: str):
    # with Session(engine) as session:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = title
    task.content = content
    session.commit()
    session.refresh(task)
    return task

def patch_task(session: SessionDep, task_id: int, new_task: TaskCrud):
    # with Session(engine) as session:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = new_task.model_dump(exclude_unset=True)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: SessionDep, task_id: int):
    # with Session(engine) as session:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
