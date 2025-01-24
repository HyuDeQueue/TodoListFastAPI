import uuid

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from src.config.security import reusable_oauth2, validate_token
from src.models.base import get_db
from src.schemas.task import TaskResponse, TaskCreateUser, TaskCreateGroup, TaskUpdate
from src.services.task_service import create_task_for_user, create_task_for_group, get_task_by_id, get_tasks_by_user_id, \
    get_tasks_by_group_id, update_task, update_task_status

router = APIRouter(prefix="/api/router", tags=["Task"])

@router.post("/user",
             response_model=TaskResponse,
             summary="Create a new task for user",
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(validate_token)])
def create_task_for_user_endpoint(task_data: TaskCreateUser,
                         db: Session = Depends(get_db)):
    return create_task_for_user(db, task_data)

@router.post("/group",
             response_model=TaskResponse,
             summary="Create a new task for group",
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(validate_token)])
def create_task_for_group_endpoint(task_data: TaskCreateGroup,
                                   db: Session = Depends(get_db)):
    return create_task_for_group(db, task_data)

@router.get("/task/{task_id}",
             response_model=TaskResponse,
             summary="Find a task by id",
             status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(validate_token)])
def find_task_endpoint(task_id: uuid.UUID, db: Session = Depends(get_db) ):
    return get_task_by_id(db, task_id)

@router.get("/user/{user_id}",
            response_model=list[TaskResponse],
            summary="Find all task by user id",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(validate_token)])
def find_user_tasks_endpoint(user_id: uuid.UUID, db: Session = Depends(get_db)):
    return get_tasks_by_user_id(db, user_id)

@router.get("/group/{group_id}",
            response_model=list[TaskResponse],
            summary="Find all task by group id",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(validate_token)])
def find_group_tasks_endpoint(group_id: uuid.UUID, db: Session = Depends(get_db)):
    return get_tasks_by_group_id(db, group_id)

@router.put("/update/{task_id}",
            response_model=TaskResponse,
            summary="Update a task by id",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(validate_token)])
def update_task_endpoint(task_id: uuid.UUID, task_data: TaskUpdate, db: Session = Depends(get_db)):
    return update_task(db, task_id, task_data)

@router.patch("/status/{task_id}/{task_status}",
               summary="Change task status",
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(validate_token)])
def delete_task_endpoint(task_id: uuid.UUID, task_status: int, db: Session = Depends(get_db)):
    update_task_status(db, task_id, task_status)