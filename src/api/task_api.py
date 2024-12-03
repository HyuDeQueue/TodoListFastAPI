import uuid

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from src.models.base import get_db
from src.schemas.task import TaskResponse, TaskCreateUser, TaskCreateGroup, TaskUpdate
from src.services.task_service import create_task_for_user, create_task_for_group, get_task_by_id, get_tasks_by_user_id, \
    get_tasks_by_group_id, update_task

router = APIRouter(prefix="/api/router", tags=["Task"])

@router.post("/user",
             response_model=TaskResponse,
             summary="Create a new task for user",
             status_code=status.HTTP_201_CREATED)
def create_task_for_user_endpoint(task_data: TaskCreateUser,
                         db: Session = Depends(get_db)):
    new_task = create_task_for_user(db, task_data)
    if not new_task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fail to create task")
    return TaskResponse.model_validate(new_task)

@router.post("/group",
             response_model=TaskResponse,
             summary="Create a new task for group",
             status_code=status.HTTP_201_CREATED)
def create_task_for_group_endpoint(task_data: TaskCreateGroup,
                                   db: Session = Depends(get_db)):
    new_task = create_task_for_group(db, task_data)
    if not new_task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fail to create task")
    return TaskResponse.model_validate(new_task)

@router.get("/task/{task_id}",
             response_model=TaskResponse,
             summary="Find a task by id",
             status_code=status.HTTP_201_CREATED)
def find_task_endpoint(task_id: uuid.UUID, db: Session = Depends(get_db) ):
    task = get_task_by_id(db, str(task_id))
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fail to find task")
    return TaskResponse.model_validate(task)

@router.get("/user/{user_id}",
            response_model=list[TaskResponse],
            summary="Find all task by user id",
            status_code=status.HTTP_200_OK)
def find_user_tasks_endpoint(user_id: uuid.UUID, db: Session = Depends(get_db)):
    tasks = get_tasks_by_user_id(db, str(user_id))
    return [TaskResponse.model_validate(task) for task in tasks]

@router.get("/group/{group_id}",
            response_model=list[TaskResponse],
            summary="Find all task by group id",
            status_code=status.HTTP_200_OK)
def find_group_tasks_endpoint(group_id: uuid.UUID, db: Session = Depends(get_db)):
    tasks = get_tasks_by_group_id(db, str(group_id))
    return [TaskResponse.model_validate(tasks) for tasks in tasks]

@router.put("/update/{task_id}",
            response_model=TaskResponse,
            summary="Update a task by id",
            status_code=status.HTTP_200_OK)
def update_task_endpoint(task_id: uuid.UUID, task_data: TaskUpdate, db: Session = Depends(get_db)):
    task = update_task(db, task_id, task_data)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fail to update task")
    return TaskResponse.model_validate(task)

@router.delete("/delete/{task_id}",
               summary="Delete a task by id",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(task_id: uuid.UUID, db: Session = Depends(get_db)):
    task = get_task_by_id(db, str(task_id))
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fail to find task")
