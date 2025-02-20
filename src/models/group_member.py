from sqlalchemy import Column, UUID, ForeignKey, String, DateTime, UniqueConstraint, func, Integer
from sqlalchemy.orm import relationship

from .base import Base
import uuid

from ..core.constants import RoleMember


class GroupMember(Base):
    __tablename__ = 'group_member'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    group_id = Column(String(36), ForeignKey('groups.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    role = Column(Integer, nullable=False, default=RoleMember.MEMBER.value)
    joined_at = Column(DateTime(timezone=True), nullable=False, default=func.now())

    group = relationship('Group', back_populates='members')
    user = relationship('User', back_populates='group_memberships')

    __table_args__ = (UniqueConstraint('group_id', 'user_id', name="unique_group_member"),)
