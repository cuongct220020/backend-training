


from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, user_id, first_name, last_name, email, password):
        self.user_id = user_id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = password
        self._user_role = None

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self._first_name} {self._last_name}, Email: {self._email}"

    @abstractmethod
    def login(self, email, password):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def update_personal_info(self):
        pass