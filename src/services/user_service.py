import uuid
from typing import Type, List

from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models import User
from src.schemas.user import UserCredential, UserLogin, UserName


def user_create(db: Session, user_data: UserCredential) -> User | None:
    user_exist = get_user_by_email(db, user_data.email)
    if not user_exist:
        new_user = User(name=user_data.name, email=user_data.email, password=bcrypt.hash(user_data.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    return None

def get_user_by_email(db: Session, email) -> Type[User] | None:
    found_user = db.query(User).filter(func.lower(User.email).like(email.lower())).first()
    return found_user

def verify_login(db: Session, user_data: UserLogin) -> User | None:
    found_user = get_user_by_email(db, user_data.email)
    if not found_user:
        return None
    elif bcrypt.verify(user_data.password, found_user.password):
        return found_user
    return None

def get_all_users(db: Session, skip: int = 0, limit: int = 10) -> list[Type[User]]:
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id = uuid.UUID) -> Type[User] | None:
    return db.query(User).filter(User.id.like(str(user_id))).first()

def update_user(db: Session, user_data: UserName, user_id: uuid.UUID) -> Type[User] | None:
    found_user = db.query(User).filter(User.id.like(str(user_id))).first()
    if found_user:
        found_user.name = user_data.name
        db.commit()
        db.refresh(found_user)
        return found_user

def delete_user(db: Session, user_id: uuid.UUID) -> Type[User] | None:
    found_user = db.query(User).filter(User.id.like(str(user_id))).first()
    if found_user:
        found_user.status = 0
        db.commit()
        return found_user
