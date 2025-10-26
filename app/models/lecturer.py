from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base


class Lecturer(Base):
    __tablename__ = 'lecturers'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    user = relationship('User', backref='lecturer')

    def __repr__(self):
        return f'<Lecturer {self.user_id}>'