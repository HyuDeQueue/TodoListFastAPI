from .auth_api import router as auth_router
from .user_api import router as user_router
from .group_api import router as group_router

routers = [auth_router,user_router,group_router]