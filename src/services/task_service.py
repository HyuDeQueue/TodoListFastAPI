from typing import Type

from sqlalchemy.orm import Session
from src.models import Task
from src.schemas.task import TaskCreateUser, TaskResponse, TaskCreateGroup, TaskUpdate


def create_task_for_user(db: Session, task_data: TaskCreateUser) -> Task:
    new_task = Task(title=task_data.title, description=task_data.description, due_time=task_data.due_time, user_id=task_data.user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def create_task_for_group(db: Session, task_data: TaskCreateGroup) -> Task:
    new_task = Task(title=task_data.title, description=task_data.description, due_time=task_data.due_time, user_id=task_data.user_id, group_id=task_data.group_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_task_by_id(db: Session, task_id: str) -> Type[Task] | None:
    task = db.query(Task).filter(Task.id == task_id,
                                 Task.status == 1).first()
    return task

def get_tasks_by_user_id(db: Session, user_id: str) -> list[Type[Task]]:
    return db.query(Task).filter(Task.user_id == user_id,
                                 Task.group_id.is_(None),
                                 Task.status == 1).all()

def get_tasks_by_group_id(db: Session, group_id: str) -> list[Task]:
    return db.query(Task).filter(Task.group_id == group_id).all()

def update_task(db: Session, task_id: str, task_data: TaskUpdate) -> Task | None:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.title = task_data.title
        task.description = task_data.description
        task.due_time = task_data.due_time
        task.completed = task_data.completed
        task.status = task_data.status
        db.commit()
        db.refresh(task)
        return task
    return None

def delete_task(db: Session, task_id: str) -> Type[Task] | None:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = 0
        db.commit()
        db.refresh(task)
        return task
    return None



