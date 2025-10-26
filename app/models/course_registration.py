
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base


class CourseRegistration(Base):
    __tablename__ = 'course_registrations'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.user_id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    student = relationship('Student', backref='registrations')
    course = relationship('Course', backref='registrations')

    def __repr__(self):
        return f'<CourseRegistration {self.id}>'