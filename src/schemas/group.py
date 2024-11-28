from datetime import datetime

from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str

class GroupResponse(GroupBase):
    id: str
    created_at: datetime
    invite_code: str
    status: int

    class Config:
        from_attributes = True