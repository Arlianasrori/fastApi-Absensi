from sqlalchemy import Column, Integer, String
from ..db.db import Base

class Developer(Base):
    __tablename__ = 'developer'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    no_telepon = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    OTP_code = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Developer(id={self.id}, username='{self.username}')>"