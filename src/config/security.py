from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from starlette import status

from src.config.config import settings


def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

def validate_token(token = Depends(reusable_oauth2)) -> str:
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

        if payload.get('exp') < datetime.now(timezone.utc).timestamp():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token expired')

        email = payload.get('sub')
        if email is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='email not found')

        return email
    except (jwt.PyJWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid token' if isinstance(e, jwt.PyJWTError) else str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
