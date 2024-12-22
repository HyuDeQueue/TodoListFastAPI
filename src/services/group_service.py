import uuid
from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.core.constants import Status
from src.models import Group
from src.schemas.group import GroupBase, GroupResponse
from src.services.group_member_service import kick_everyone_in_group


def create_group(db: Session, group_data: GroupBase) -> GroupResponse:
    new_group = Group(name=group_data.name)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return GroupResponse.model_validate(new_group)

def get_all_groups(db: Session, skip: int = 0, limit: int = 10) -> list[GroupResponse]:
    groups = db.query(Group).offset(skip).limit(limit).filter(Group.status == Status.ACTIVE.value).all()
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
        group.status = Status.DELETED.value
        kick_everyone_in_group(db, group_id)
        db.commit()


