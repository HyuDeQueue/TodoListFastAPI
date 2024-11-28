import uuid

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import nullsfirst
from starlette import status

from src.models.base import get_db
from src.schemas.group import GroupResponse
from src.services.group_service import *

router = APIRouter(prefix="/api/group", tags=["Groups"])

@router.post("/",
             response_model=GroupResponse,
             summary="Create a group",
             status_code=status.HTTP_201_CREATED)
def create_group_endpoint(group_data: GroupBase,
                          db: Session = Depends(get_db)):
    new_group = create_group(db, group_data)
    if not new_group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create group")
    return GroupResponse.model_validate(new_group)

@router.get("/",
            response_model=list[GroupResponse],
            summary="Get all groups",
            status_code=status.HTTP_200_OK)
def get_all_groups_endpoint(skip: int = 0, take: int = 10,db: Session = Depends(get_db)):
    groups = get_all_groups(db, skip, take)
    return [GroupResponse.model_validate(group) for group in groups]

@router.get("/{group_id}",
            response_model=GroupResponse,
            summary="Get a specific group",
            status_code=status.HTTP_200_OK)
def get_group_endpoint(group_id: uuid.UUID, db: Session = Depends(get_db)):
    group = get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    else:
        return GroupResponse.model_validate(group)

@router.put("/{group_id}",
            response_model=GroupResponse,
            summary="Update a group",
            status_code=status.HTTP_200_OK)
def update_group_endpoint(group_id: uuid.UUID,
                          group_data: GroupBase,
                          db: Session = Depends(get_db)):
    group = update_group(db, group_id, group_data)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found for updating")
    else:
        return GroupResponse.model_validate(group)

@router.delete("/{group_id}",
               summary="Delete a group",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_group_endpoint(group_id: uuid.UUID, db: Session = Depends(get_db)):
    group = delete_group(db, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found for deleting")
    else:
        return None