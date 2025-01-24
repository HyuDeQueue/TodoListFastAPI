from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str
    due_time: datetime
    priority: int

class TaskCreateUser(TaskBase):
    user_id: str

class TaskCreateGroup(TaskCreateUser):
    group_id: str

class TaskUpdate(TaskBase):
    completed: bool
    status: str
    priority: int

class TaskResponse(TaskBase):
    id: str
    created_at: datetime
    due_time: datetime
    completed: bool
    priority: int
    status: int
    user_id: str
    group_id: str
    class Config:
        from_attributes = True
