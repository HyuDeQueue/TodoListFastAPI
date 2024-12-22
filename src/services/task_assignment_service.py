import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.models import TaskAssignment
from src.schemas.task_assignment import TaskAssignmentBase, TaskAssignmentResponse


def assign_task(db: Session, task_id: uuid.UUID , user_id: uuid.UUID) -> TaskAssignmentResponse:
    new_assignment = TaskAssignment(task_id = str(task_id),user_id = str(user_id))
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return TaskAssignmentResponse.model_validate(new_assignment)

def change_assign_user(db: Session, task_id: uuid.UUID , user_id: uuid.UUID, new_user_id: uuid.UUID) -> TaskAssignmentResponse:
    saved_assignment = db.query(TaskAssignment).filter_by(task_id = str(task_id),user_id = str(user_id)).first()
    saved_assignment.task_id = str(new_user_id)
    db.commit()
    db.refresh(saved_assignment)
    return TaskAssignmentResponse.model_validate(saved_assignment)

def unassign_task(db: Session, task_id: uuid.UUID , user_id: uuid.UUID):
    saved_assignment = db.query(TaskAssignment).filter_by(task_id = str(task_id),user_id = str(user_id)).first()
    db.delete(saved_assignment)
    db.commit()

