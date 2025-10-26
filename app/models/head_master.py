from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base


class HeadMaster(Base):
    __tablename__ = 'head_masters'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship('User', backref='head_master')

    def __repr__(self):
        return f'<HeadMaster {self.user_id}>'
