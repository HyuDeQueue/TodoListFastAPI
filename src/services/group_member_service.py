import uuid
from tokenize import group

from alembic.util import status
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from starlette.status import HTTP_403_FORBIDDEN

from src.core.constants import RoleMember, GeneralStatus
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
    members = db.query(GroupMember).filter_by(group_id=group_member_data.group_id).order_by(GroupMember.joined_at).all()
    if len(members) == 1:
        this_group = db.query(Group).filter_by(id=group_member_data.group_id).first()
        this_group.status = GeneralStatus.DELETED.value
        db.delete(group_member)
        db.commit()
        return {"message": "Group deleted as it had only one member"}

    if group_member.role == RoleMember.ADMIN.value:
        members[1].role = RoleMember.ADMIN.value
        db.commit()
    db.delete(group_member)
    db.commit()
    return {"message": "Member removed successfully"}

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

def apply_invite_code(db: Session, invite_code: str, user_id: uuid.UUID):
    found_group = db.query(Group).filter_by(invite_code=invite_code).first()
    if not found_group:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invite code does not exist")
    found_user = db.query(User).filter_by(id=user_id).first()
    if not found_user:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User does not exist")
    group_member = GroupMember(group_id=str(found_group.id), user_id=str(found_user.id), role=RoleMember.MEMBER.value)
    db.add(group_member)
    db.commit()
    db.refresh(group_member)
    return GroupMemberResponse.model_validate(group_member)

