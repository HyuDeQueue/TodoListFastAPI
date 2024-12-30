from enum import Enum


class GeneralStatus(Enum):
    DELETED = 0
    ACTIVE = 1
    ASSIGNED = 2
    COMPLETED = 3

class RoleMember(Enum):
    MEMBER = 0
    ADMIN = 1

class TaskPriority(Enum):
    NO_CONCERN = 0
    LOW = 1
    NORMAL = 2
    HIGH = 3
    MUST_DO = 4

class UserPermission(Enum):
    USER = 0
    PREMIUM = 1
    ADMIN = 2

# More ideas will be add here


