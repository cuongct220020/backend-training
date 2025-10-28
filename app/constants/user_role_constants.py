# app/constants/user_role_constants.py
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    STUDENT = "student"
    LECTURER = "lecturer"
    HEADMASTER = "headmaster"
