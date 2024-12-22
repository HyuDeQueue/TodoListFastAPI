from enum import Enum


class Status(Enum):
    DELETED = 0
    ACTIVE = 1
    ASSIGNED = 2
    COMPLETED = 3

class RoleUser(Enum):
    ADMIN = 'admin'
    MEMBER = 'member'
