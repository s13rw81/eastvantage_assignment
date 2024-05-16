# user_management/models.py
from config import BASE
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(BASE):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    addresses = relationship("Address", back_populates="user")


