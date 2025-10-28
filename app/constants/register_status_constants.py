# app/constants/register_status_constants.py
from enum import Enum


class RegistrationStatus(Enum):
    REGISTERED = "registered"
    FULLED = "fulled"
    CANCELLED = "cancelled"
