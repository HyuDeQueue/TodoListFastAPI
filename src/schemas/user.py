from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str

class UserLogin(UserBase):
    password: str

class UserCredential(UserBase):
    name: str
    password: str

class UserName(BaseModel):
    name: str


class UserResponse(UserBase):
    id: str
    name: str
    created_at: datetime
    status: int

    class Config:
        orm_mode = True