from sys import prefix

from fastapi import APIRouter

router = APIRouter(prefix="/group-member", tags=["group-member"])
