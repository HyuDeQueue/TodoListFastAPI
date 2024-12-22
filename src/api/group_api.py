import uuid

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import nullsfirst
from starlette import status

from src.config.security import reusable_oauth2, validate_token
from src.models.base import get_db
from src.schemas.group import GroupResponse
from src.services.group_service import *

router = APIRouter(prefix="/api/group", tags=["Groups"])

@router.post("/",
             response_model=GroupResponse,
             summary="Create a group",
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(validate_token)])
def create_group_endpoint(group_data: GroupBase, created_by: uuid.UUID,
                          db: Session = Depends(get_db)):
    return create_group(db, group_data, created_by)

@router.get("/",
            response_model=list[GroupResponse],
            summary="Get all groups",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(validate_token)])
def get_all_groups_endpoint(skip: int = 0, take: int = 10,db: Session = Depends(get_db)):
    return get_all_groups(db, skip, take)

@router.get("/{group_id}",
            response_model=GroupResponse,
            summary="Get a specific group",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(validate_token)])
def get_group_endpoint(group_id: uuid.UUID, db: Session = Depends(get_db)):
    return get_group_by_id(db, group_id)

@router.put("/{group_id}",
            response_model=GroupResponse,
            summary="Update a group",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(validate_token)])
def update_group_endpoint(group_id: uuid.UUID,
                          group_data: GroupBase,
                          db: Session = Depends(get_db)):
    return update_group(db, group_id, group_data)

@router.delete("/{group_id}",
               summary="Delete a group",
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(validate_token)])
def delete_group_endpoint(group_id: uuid.UUID, db: Session = Depends(get_db)):
    delete_group(db, group_id)
