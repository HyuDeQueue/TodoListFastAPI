import uuid
from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from src.core.constants import GeneralStatus
from src.models import Task
from src.schemas.task import TaskCreateUser, TaskResponse, TaskCreateGroup, TaskUpdate


def create_task_for_user(db: Session, task_data: TaskCreateUser) -> TaskResponse:
    new_task = Task(title=task_data.title, description=task_data.description, due_time=task_data.due_time, user_id=task_data.user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return TaskResponse.model_validate(new_task)

def create_task_for_group(db: Session, task_data: TaskCreateGroup) -> TaskResponse:
    new_task = Task(title=task_data.title, description=task_data.description, due_time=task_data.due_time, user_id=task_data.user_id, group_id=task_data.group_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return TaskResponse.model_validate(new_task)

def get_task_by_id(db: Session, task_id: uuid.UUID) -> TaskResponse:
    task = db.query(Task).filter(Task.id == str(task_id)).first()
    if not task:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Task not found')
    return TaskResponse.model_validate(task)

def get_tasks_by_user_id(db: Session, user_id: uuid.UUID) -> list[TaskResponse]:
    tasks = db.query(Task).filter(Task.user_id is str(user_id),
                                 Task.group_id.is_(None)).all()
    return [TaskResponse.model_validate(task) for task in tasks]

def get_tasks_by_group_id(db: Session, group_id: uuid.UUID) -> list[TaskResponse]:
    tasks = db.query(Task).filter(Task.group_id is str(group_id)).all()
    return [TaskResponse.model_validate(task) for task in tasks]


def update_task(db: Session, task_id: uuid.UUID, task_data: TaskUpdate) -> TaskResponse:
    task = db.query(Task).filter(Task.id is str(task_id)).first()
    if not task:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Task not found')
    else:
        task.title = task_data.title
        task.description = task_data.description
        task.due_time = task_data.due_time
        task.completed = task_data.completed
        task.status = task_data.status
        db.commit()
        db.refresh(task)
        return TaskResponse.model_validate(task)

def delete_task(db: Session, task_id: uuid.UUID):
    task = db.query(Task).filter(Task.id is str(task_id)).first()
    if not task:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Task not found')
    if task:
        task.status = GeneralStatus.DELETED.value
        db.commit()



