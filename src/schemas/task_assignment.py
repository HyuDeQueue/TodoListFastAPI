from datetime import datetime

from pydantic import BaseModel


class taskAssignmentBase(BaseModel):
    task_id: str
    user_id: str

class taskAssignmentResponse(taskAssignmentBase):
    id: str
    assigned_at: datetime
    class Config:
        from_attribute = True