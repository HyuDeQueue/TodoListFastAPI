import uuid

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST

from src.config.security import reusable_oauth2, validate_token
from src.models.base import get_db
from src.schemas.task_assignment import TaskAssignmentResponse
from src.services.task_assignment_service import assign_task, change_assign_user, unassign_task

router = APIRouter(prefix="/api/task_assign", tags=["TaskAssignment"])

@router.post("/assign/{task_id}/{user_id}",
             response_model=TaskAssignmentResponse,
             summary="Create a new TaskAssignment",
             description="Create a new TaskAssignment",
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(validate_token)])
def assign_member_endpoint(task_id: uuid.UUID, user_id: uuid.UUID, db: Session = Depends(get_db)):
    return assign_task(db, task_id, user_id)

@router.put("/update/{task_id}/{user_id}/to/{new_user_id}",
            response_model=TaskAssignmentResponse,
            summary="Update a TaskAssignment",
            description="Update a TaskAssignment",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(validate_token)])
def reassign_member_endpoint(task_id: uuid.UUID, user_id: uuid.UUID, new_user_id: uuid.UUID, db:Session = Depends(get_db)):
    return change_assign_user(db, task_id, user_id, new_user_id)

@router.delete("/delete/{task_id}/{user_id}",
               response_model=TaskAssignmentResponse,
               summary="Unassign a member",
               description="Unassign a member",
               status_code=status.HTTP_200_OK,
               dependencies=[Depends(validate_token)])
def unassign_member_endpoint(task_id: uuid.UUID, user_id: uuid.UUID, db:Session = Depends(get_db)):
    unassign_task(db, task_id, user_id)



