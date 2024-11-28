import uuid
from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models import Group
from src.schemas.group import GroupBase


def create_group(db: Session, group_data: GroupBase) -> Group:
    new_group = Group(name=group_data.name)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

def get_all_groups(db: Session, skip: int = 0, limit: int = 10) -> list[Type[Group]]:
    return db.query(Group).offset(skip).limit(limit).all()

def get_group_by_id(db: Session, group_id: uuid.UUID) -> Type[Group] | None:
    return db.query(Group).filter(Group.id.like(str(group_id))).first()

def update_group(db: Session, group_id: uuid.UUID, group_data: GroupBase) -> Type[Group]:
    group = db.query(Group).filter(Group.id.like(str(group_id))).first()
    if group:
        group.name = group_data.name
        db.commit()
        db.refresh(group)
        return group

def delete_group(db: Session, group_id: uuid.UUID) -> Type[Group]:
    group = db.query(Group).filter(Group.id.like(str(group_id))).first()
    if group:
        db.delete(group)
        db.commit()
        return group


