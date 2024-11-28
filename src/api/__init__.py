from .group_api import router as group_router
from .user_api import router as user_router

routers = [group_router, user_router]