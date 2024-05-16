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

    def __str__(self):
        return f"<User: id: {self.id} name = {self.first_name} + " " + {self.last_name} email: {self.email}>"

    def __repr__(self):
        return self.__str__()
