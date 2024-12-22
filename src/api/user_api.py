import uuid
from pydoc import describe
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from src.config.security import reusable_oauth2, validate_token
from src.models.base import get_db
from src.schemas.user import UserResponse, UserLogin, UserCredential, UserName
from src.services.user_service import verify_login, user_create, get_all_users, get_user_by_id, update_user, delete_user

router = APIRouter(prefix="/api/user", tags=["Users"])

@router.get("/",
            response_model=list[UserResponse],
            summary="Get all users",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(validate_token)])
def get_all_users_endpoint(skip: int = 0, take: int = 10 ,db: Session = Depends(get_db)):
    return get_all_users(db, skip, take)

@router.get("/{user_id}",
            response_model=UserResponse,
            summary="Get a specific user",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(validate_token)])
def get_user_endpoint(user_id: uuid.UUID,db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)



@router.put("/{user_id}",
            response_model=UserResponse,
            summary="Update a specific user",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(validate_token)])
def update_user_endpoint(user_id: uuid.UUID,
                         user_data: UserName,
                         db: Session = Depends(get_db)):
    return update_user(db, user_data, user_id)

@router.delete("/{user_id}",
               summary="Ban a specific user",
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(validate_token)])
def delete_user_endpoint(user_id: uuid.UUID, ban_reason: Optional[str] = Query("Just banned", description="Reason for banning"),db: Session = Depends(get_db)):
    delete_user(db, user_id, ban_reason)




