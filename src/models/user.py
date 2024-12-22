from datetime import datetime

from alembic.util import status
from sqlalchemy.orm import relationship

from .base import Base
import uuid
from sqlalchemy import UUID, Column, String, func, DateTime, INTEGER

from ..core.constants import Status


class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    status = Column(INTEGER, nullable=False, default=Status.ACTIVE.value)
    ban_reason = Column(String(255), nullable=True)

    tasks = relationship("Task", back_populates="user", cascade="all, delete")
    group_memberships = relationship("GroupMember", back_populates="user", cascade="all, delete")
    task_assignment = relationship("TaskAssignment", back_populates="user",)
