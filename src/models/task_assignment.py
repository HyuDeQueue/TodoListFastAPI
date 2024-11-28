from datetime import datetime

from sqlalchemy.orm import relationship

from .base import Base
import uuid

from sqlalchemy import UUID, Column, ForeignKey, DateTime, UniqueConstraint, func, String


class TaskAssignment(Base):
    __tablename__ = 'task_assignment'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String(36), ForeignKey('tasks.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), default=func.now())

    tasks = relationship('Task', back_populates='task_assignment')
    user = relationship('User', back_populates='task_assignment')

    __table_args__ = (UniqueConstraint('task_id', 'user_id', name= "unique_task_user"),)