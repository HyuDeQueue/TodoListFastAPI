import uuid
from typing import Type, List

from fastapi import HTTPException
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from src.core.constants import GeneralStatus
from src.models import User
from src.schemas.user import UserCredential, UserLogin, UserName, UserResponse


def user_create(db: Session, user_data: UserCredential) -> UserResponse:
    user_exist = get_user_by_email(db, user_data.email)
    if user_exist:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Email already registered')
    else:
        new_user = User(name=user_data.name, email=user_data.email, password=bcrypt.hash(user_data.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserResponse.model_validate(new_user)

def get_user_by_email(db: Session, email) -> UserResponse:
    found_user = db.query(User).filter(func.lower(User.email).like(email.lower())).first()
    if not found_user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Email not found')
    return UserResponse.model_validate(found_user)

def verify_login(db: Session, user_data: UserLogin) -> UserResponse:
    found_user = get_user_by_email(db, user_data.email)
    if not bcrypt.verify(user_data.password, bytes(user_data.password, 'utf-8')):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Incorrect password')
    elif found_user.status != GeneralStatus.ACTIVE:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='User is banned')
    else:
        return UserResponse.model_validate(found_user)

def get_all_users(db: Session, skip: int = 0, limit: int = 10) -> list[UserResponse]:
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserResponse.model_validate(user) for user in users]


def get_all_active_users(db: Session, skip: int = 0, limit: int = 10) -> list[UserResponse]:
    users = db.query(User).offset(skip).limit(limit).filter(User.status == GeneralStatus.ACTIVE.value).all()
    return [UserResponse.model_validate(user) for user in users]

def get_user_by_id(db: Session, user_id = uuid.UUID) -> UserResponse:
    found_user = db.query(User).filter(User.id is user_id).first()
    if not found_user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='User not found')
    return UserResponse.model_validate(found_user)

def update_user(db: Session, user_data: UserName, user_id: uuid.UUID) -> UserResponse:
    found_user = db.query(User).filter(User.id is str(user_id)).first()
    if not found_user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='User not found')
    else:
        found_user.name = user_data.name
        db.commit()
        db.refresh(found_user)
        return UserResponse.model_validate(found_user)

def delete_user(db: Session, user_id: uuid.UUID, ban_reason: str):
    found_user = db.query(User).filter(User.id is str(user_id)).first()
    if not found_user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='User not found')
    else:
        found_user.ban_reason = ban_reason
        found_user.status = GeneralStatus.DELETED.value
        db.commit()