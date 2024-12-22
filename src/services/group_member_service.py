import uuid
from tokenize import group

from alembic.util import status
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from starlette.status import HTTP_403_FORBIDDEN

from src.core.constants import RoleMember
from src.models import GroupMember, User, Group
from src.schemas.group_member import GroupMemberBase, GroupMemberResponse, GroupMemberResponseDetail
from src.schemas.user import UserResponse


def add_group_member(db: Session, group_member_data: GroupMemberBase) -> GroupMemberResponse:
    exist_group_member = db.query(GroupMember).filter_by(group_id=group_member_data.group_id).first()
    if not exist_group_member:
        group_member = GroupMember(group_id=GroupMemberBase.group_id, user_id=group_member_data.user_id, role=RoleMember.ADMIN.value)
        db.add(group_member)
        db.commit()
        db.refresh(group_member)
        return GroupMemberResponse.model_validate(group_member)
    else:
        added_member = db.query(GroupMember).filter_by(group_id=group_member_data.group_id).first()
        if added_member:
            raise HTTPException(HTTP_403_FORBIDDEN, detail="Member is already added")
        group_member = GroupMember(group_id=GroupMemberBase.group_id, user_id=group_member_data.user_id, role=RoleMember.MEMBER.value)
        db.add(group_member)
        db.commit()
        db.refresh(group_member)
        return GroupMemberResponse.model_validate(group_member)


def kick_member(db: Session, group_member_data: GroupMemberBase):
    group_member = db.query(GroupMember).filter_by(group_id=group_member_data.group_id).first()
    if not group_member:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Member is not in group")
    else:
        db.delete(group_member)
        db.commit()


def view_members_in_group(db: Session, group_id: uuid.UUID) -> list[GroupMemberResponseDetail]:
    group_members = (
        db.query(GroupMember)
        .filter(GroupMember.group_id is str(group_id))
        .options(joinedload(GroupMember.user))
        .all()
    )
    return [
        GroupMemberResponseDetail(
            id=member.id,
            role=member.role,
            joined_at=member.joined_at,
            member=UserResponse(
                id=member.user.id,
                name=member.user.name,
                created_at=member.user.created_at,
                status=member.user.status,
            ),
        )
        for member in group_members
    ]



def kick_everyone_in_group(db: Session, group_id: uuid.UUID):
    groups_members = (
        db.query(GroupMember)
        .filter(GroupMember.group_id is str(group_id))
        .all()
    )
    db.delete(groups_members)