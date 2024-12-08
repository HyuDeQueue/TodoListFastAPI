from tokenize import group

from alembic.util import status
from sqlalchemy.orm import Session, joinedload

from src.models import GroupMember, User, Group
from src.schemas.group_member import GroupMemberBase, GroupMemberResponse, GroupMemberResponseDetail
from src.schemas.user import UserResponse




def add_group_member(db: Session, group_member_data: GroupMemberBase) -> GroupMember | None:
    exist_group_member = db.query(GroupMember).filter_by(group_id=group_member_data.group_id).first()
    if not exist_group_member:
        group_member = GroupMember(group_id=GroupMemberBase.group_id, user_id=group_member_data.user_id, role="admin")
        db.add(group_member)
        db.commit()
        db.refresh(group_member)
        return group_member
    else:
        added_member = db.query(GroupMember).filter_by(group_id=group_member_data.group_id).first()
        if added_member:
            return None
        group_member = GroupMember(group_id=GroupMemberBase.group_id, user_id=group_member_data.user_id, role="member")
        db.add(group_member)
        db.commit()
        db.refresh(group_member)
        return group_member


def kick_member(db: Session, group_member_data: GroupMemberBase):
    group_member = db.query(GroupMember).filter_by(group_id=group_member_data.group_id).first()
    if group_member:
        db.delete(group_member)
        db.commit()
        db.refresh(group_member)
        return group_member
    

def view_members_in_group(db: Session, group_id: str) -> list[GroupMember]:
    group_members = (
        db.query(GroupMember)
        .filter(GroupMember.group_id == group_id)
        .options(joinedload(GroupMember.user))
        .all()
    )
    return group_members