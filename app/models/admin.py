from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base


class Admin(Base):
    __tablename__ = 'admins'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    user = relationship('User', backref='admin')

    def __repr__(self):
        return f'<Admin {self.user_id}>'