from app.models.user import User


class Lecturer(User):
    def __init__(self, user_id, first_name, last_name, email, password):
        super().__init__(user_id, first_name, last_name, email, password)
        self._user_role = 'lecturer'

    def login(self, email, password):
        # Implementation for lecturer login
        pass

    def register(self):
        # Implementation for lecturer registration
        pass

    def update_personal_info(self):
        # Implementation for updating lecturer personal info
        pass