

from sqlalchemy import Column, Integer, String, Text
from app.extensions import Base


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)

    def __repr__(self):
        return f'<Course {self.name}>'