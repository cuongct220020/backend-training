from app.models.user import User


class Admin(User):
    def __init__(self, user_id, first_name, last_name, email, password):
        super().__init__(user_id, first_name, last_name, email, password)
        self._user_role = 'admin'

    def login(self, email, password):
        # Implementation for admin login
        pass

    def register(self):
        # Implementation for admin registration
        pass

    def update_personal_info(self):
        # Implementation for updating admin personal info
        pass