from sqlalchemy import Column, Integer, String
from app.extensions import Base


class Classroom(Base):
    __tablename__ = 'classrooms'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    def __repr__(self):
        return f'<Classroom {self.name}>'