from pydantic import BaseModel

from src.schemas.user import UserResponse


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(BaseModel):
    user: UserResponse
    token: Token

    class Config:
        from_attributes = True