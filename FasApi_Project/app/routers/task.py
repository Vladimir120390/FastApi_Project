from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
router = APIRouter()

@router.get("/")
def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.execute(select(Task)).scalars().all()
    return tasks

@router.get("/{task_id}")
def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    return task

@router.post("/create")
def create_task(task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    # Проверка на существование пользователя
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    new_task = Task(
        title=task.title,
        content=task.content,
        priority=task.priority,
        user_id=user_id
    )

    db.execute(insert(Task).values(
        title=new_task.title,
        content=new_task.content,
        priority=new_task.priority,
        user_id=new_task.user_id
    ))

    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update")
def update_task(task_id: int, task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    existing_task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    db.execute(update(Task).where(Task.id == task_id).values(
        title=task.title,
        content=task.content,
        priority=task.priority
    ))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}

@router.delete("/delete")
def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    existing_task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task deleted successfully!'}
