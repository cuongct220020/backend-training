from sqlalchemy import Column, Integer, String
from app.extensions import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    email = Column(String(255), unique=True)
    user_role = Column(String(50))

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'