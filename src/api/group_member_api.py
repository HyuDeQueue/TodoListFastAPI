import uuid
from sys import prefix

from sqlalchemy.orm import Session
from starlette import status

from src.config.security import reusable_oauth2, validate_token
from src.models.base import get_db
from fastapi import APIRouter, Depends

from src.schemas.group_member import GroupMemberResponse, GroupMemberBase, GroupMemberResponseDetail
from src.services.group_member_service import add_group_member, kick_member, view_members_in_group

router = APIRouter(prefix="/group-member", tags=["group-member"])

@router.post("add",
             response_model=GroupMemberResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Add a group member",
             description="Add a group member",
             dependencies=[Depends(validate_token)])
def add_group_member_endpoint(group_member_data: GroupMemberBase, db: Session = Depends(get_db)):
    new_group_member = add_group_member(db, group_member_data)
    return GroupMemberResponse.model_validate(new_group_member)

@router.delete("delete",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a group member",
               description="Delete a group member",
               dependencies=[Depends(validate_token)])
def kick_group_member_endpoint(group_member_data: GroupMemberBase, db: Session = Depends(get_db)):
    found_group_member = kick_member(db, group_member_data)

@router.get("view",
            response_model=GroupMemberResponseDetail,
            status_code=status.HTTP_200_OK,
            summary="View a group member",
            description="View a group member",
            dependencies=[Depends(validate_token)])
def view_members_endpoint(group_id: uuid.UUID ,db: Session = Depends(get_db)):
    group_members = view_members_in_group(db, str(group_id))
    if group_members:
        return GroupMemberResponseDetail.model_validate(group_members)