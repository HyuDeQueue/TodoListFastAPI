from sqlalchemy.orm import Session

from src.models import TaskAssignment
from src.schemas.task_assignment import taskAssignmentBase


def assign_task(db: Session, task_id: str , user_id: str) -> TaskAssignment:
    new_assignment = TaskAssignment(task_id = task_id,user_id = user_id)
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

def change_assign_user(db: Session, task_id: str , user_id: str, new_user_id: str) -> TaskAssignment | None:
    saved_assignment = db.query(TaskAssignment).filter_by(task_id = task_id,user_id = user_id).first()
    saved_assignment.task_id = new_user_id
    db.commit()
    db.refresh(saved_assignment)
    return saved_assignment

def unassign_task(db: Session, task_id: str , user_id: str):
    saved_assignment = db.query(TaskAssignment).filter_by(task_id = task_id,user_id = user_id).first()
    db.delete(saved_assignment)
    db.commit()
    return

