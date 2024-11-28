import uuid

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from src.models.base import get_db
from src.schemas.user import UserResponse, UserLogin, UserCredential, UserName
from src.services.user_service import verify_login, user_create, get_all_users, get_user_by_id, update_user, delete_user

router = APIRouter(prefix="/api/user", tags=["Users"])

@router.get("/",
            response_model=list[UserResponse],
            summary="Get all users",
            status_code=status.HTTP_200_OK)
def get_all_users_endpoint(skip: int = 0, take: int = 10 ,db: Session = Depends(get_db)):
    users_list = get_all_users(db, skip, take)
    return [UserResponse.model_validate(user) for user in users_list]

@router.get("/{user_id}",
             response_model=UserResponse,
             summary="Get a specific user",
             status_code=status.HTTP_200_OK)
def get_user_endpoint(user_id: uuid.UUID,db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "User does not exist")
    else:
        return UserResponse.model_validate(user)


@router.put("/{user_id}",
            response_model=UserResponse,
            summary="Update a specific user",
            status_code=status.HTTP_200_OK)
def update_user_endpoint(user_id: uuid.UUID,
                         user_data: UserName,
                         db: Session = Depends(get_db)):
    user = update_user(db, user_data, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "User does not exist")
    else:
        return UserResponse.model_validate(user)

@router.delete("/{user_id}",
               summary="Delete a specific user",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: uuid.UUID,db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "User does not exist")
    else:
        return None




