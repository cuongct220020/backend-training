from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base


class Student(Base):
    __tablename__ = 'students'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    address = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    department = Column(String(255), nullable=True)
    major = Column(String(255), nullable=True)
    enrollment_year = Column(Integer, nullable=True)
    class_id = Column(Integer, nullable=True)
    user = relationship('User', backref='student')

    def __repr__(self):
        return f'<Student {self.user_id}>'


