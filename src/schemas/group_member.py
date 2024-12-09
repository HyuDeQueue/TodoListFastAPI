from datetime import datetime

from pydantic import BaseModel

from src.schemas.user import UserResponse


class GroupMemberBase(BaseModel):
    group_id: str
    user_id: str

class GroupMemberResponse(GroupMemberBase):
    id: str
    role: str
    joined_at: datetime
    class Config:
        orm_mode: True

class GroupMemberResponseDetail(BaseModel):
    id: str
    group_id: str
    role: str
    joined_at: datetime
    member: UserResponse
    class Config:
        orm_mode = True