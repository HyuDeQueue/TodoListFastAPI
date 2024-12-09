from datetime import datetime

from pydantic import BaseModel


class TaskAssignmentBase(BaseModel):
    task_id: str
    user_id: str

class TaskAssignmentResponse(TaskAssignmentBase):
    id: str
    assigned_at: datetime
    class Config:
        from_attribute = True