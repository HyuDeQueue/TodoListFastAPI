from .auth_api import router as auth_router
from .user_api import router as user_router
from .group_api import router as group_router
from .task_api import router as task_router
from .task_assignment_api import router as assign_router
from .group_member_api import router as member_router

routers = [auth_router,user_router,group_router,task_router,assign_router, member_router]