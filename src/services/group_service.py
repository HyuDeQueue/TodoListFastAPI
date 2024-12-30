import uuid
from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.core.constants import GeneralStatus
from src.models import Group, group
from src.schemas.group import GroupBase, GroupResponse
from src.schemas.group_member import GroupMemberBase
from src.services.group_member_service import kick_everyone_in_group, add_group_member


def create_group(db: Session, group_data: GroupBase, created_by: uuid.UUID) -> GroupResponse:
    new_group = Group(name=group_data.name, created_by=str(created_by))
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    add_group_member(db, GroupMemberBase(group_id= str(new_group.id), user_id = str(created_by)))
    return GroupResponse.model_validate(new_group)

def get_all_groups(db: Session, skip: int = 0, limit: int = 10) -> list[GroupResponse]:
    groups = db.query(Group).offset(skip).limit(limit).filter(Group.status == GeneralStatus.ACTIVE.value).all()
    return [GroupResponse.model_validate(group) for group in groups]

def get_group_by_id(db: Session, group_id: uuid.UUID) -> GroupResponse:
    group = db.query(Group).filter(Group.id.like(str(group_id))).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return GroupResponse.model_validate(group)

def update_group(db: Session, group_id: uuid.UUID, group_data: GroupBase) -> GroupResponse:
    group = db.query(Group).filter(Group.id is str(group_id)).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    else:
        group.name = group_data.name
        db.commit()
        db.refresh(group)
        return GroupResponse.model_validate(group)

def delete_group(db: Session, group_id: uuid.UUID):
    group = db.query(Group).filter(Group.id is str(group_id)).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    else:
        group.status = GeneralStatus.DELETED.value
        kick_everyone_in_group(db, group_id)
        db.commit()

def change_invite_code(db: Session, invite_code: str, group_id: uuid.UUID) -> GroupResponse:
    found_group = db.query(Group).filter(Group.id is str(group_id)).first()
    if not found_group:
        raise HTTPException(status_code=404, detail="Group not found")
    found_group.invite_code = invite_code
    db.commit()
    db.refresh(found_group)
    return GroupResponse.model_validate(found_group)

