import string

from app.models.user import User


class Student(User):
    def __init__(self, user_id, first_name, last_name, email, password):
        super().__init__(user_id, first_name, last_name, email, password)
        self._user_role = 'student'
        self._age = None
        self._gender = None
        self._address = None
        self._phone = None
        self._department = None
        self._major = None
        self._enrollment_year = None
        self._class_id = None
        self._timetable = []

    def login(self, email, password):
        # Implementation for student login
        pass

    def register(self):
        # Implementation for student registration
        pass

    def update_personal_info(self):
        # Implementation for updating student personal info
        pass

    def create_personal_info(self):
        pass

    def view_timetable(self):
        pass

    def create_course_registration(self):
        pass

    def delete_course_registration(self):
        pass

