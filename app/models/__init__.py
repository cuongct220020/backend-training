from .user import User
from .classroom import Classroom
from .course import Course
from .course_registration import CourseRegistration
from .lecturer import Lecturer
from .student import Student
from .subject import Subject
from .timetable import Timetable
from .address import Address
from .admin import Admin

__all__ = [
    'User',
    'Admin',
    'Classroom',
    'Course',
    'CourseRegistration',
    'Lecturer',
    'Student',
    'Subject',
    'Timetable',
    'Address'
]