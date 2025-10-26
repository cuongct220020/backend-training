

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship('Course', backref='subjects')

    def __repr__(self):
        return f'<Subject {self.name}>'