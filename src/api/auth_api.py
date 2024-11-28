from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.config.security import create_jwt_token
from src.models.base import get_db
from src.schemas.auth import LoginResponse, Token
from src.schemas.user import UserResponse, UserLogin, UserCredential
from starlette import status

from src.services.user_service import verify_login, user_create

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse, summary="Login user", status_code=status.HTTP_200_OK)
def user_login_endpoint(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = verify_login(db, user_credentials)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login information")

    access_token = create_jwt_token(data={"sub": user.email})

    user_response = UserResponse.model_validate(user)
    return LoginResponse(user=user_response, token=Token(access_token=access_token, token_type="Bearer"))


@router.post("/register",
             response_model=UserResponse,
             summary="Register user",
             status_code=status.HTTP_200_OK)
def user_register_endpoint(user_credentials: UserCredential, db: Session = Depends(get_db)):
    user = user_create(db, user_credentials)
    if not user:
        raise HTTPException(status_code=400,detail= "User already exist with this email")
    return UserResponse.model_validate(user)