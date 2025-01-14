
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .base import Base
import uuid
from sqlalchemy import UUID, Column, String, DateTime, func, ForeignKey

from ..core.constants import GeneralStatus


class Group(Base):
    __tablename__ = 'groups'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    invite_code = Column(String(36), default=lambda: str(uuid.uuid4()))
    status = Column(INTEGER, nullable=False, default=GeneralStatus.ACTIVE.value)
    created_by = Column(String(36),ForeignKey('users.id'), nullable=False)

    creator = relationship('User', backref="created_groups")
    members = relationship('GroupMember', back_populates='group', cascade='all, delete')
    tasks = relationship('Task', back_populates='group', cascade='all, delete')
