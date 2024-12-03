from datetime import datetime
from time import timezone

from faker.providers.date_time import datetime_to_timestamp
from sqlalchemy.orm import relationship

from .base import Base
import uuid
from sqlalchemy import UUID, Column, String, DateTime, Boolean, func, ForeignKey, INTEGER


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    due_time = Column(DateTime(timezone=True))
    completed = Column(Boolean, default=False)
    status = Column(INTEGER, nullable=False, default=1)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    group_id = Column(String(36), ForeignKey('groups.id'))

    task_assignment = relationship("TaskAssignment", back_populates="tasks", cascade="all, delete-orphan")
    user = relationship("User", back_populates="tasks")
    group = relationship("Group", back_populates="tasks")

