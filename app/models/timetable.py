


from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base


class TimeTable(Base):
    __tablename__ = 'timetables'
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    lecturer_id = Column(Integer, ForeignKey('lecturers.user_id'))
    classroom_id = Column(Integer, ForeignKey('classrooms.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    subject = relationship('Subject', backref='timetables')
    lecturer = relationship('Lecturer', backref='timetables')
    classroom = relationship('Classroom', backref='timetables')

    def __repr__(self):
        return f'<TimeTable {self.id}>'