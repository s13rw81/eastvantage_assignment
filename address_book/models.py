# address_book/models.py
from config import BASE
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from user_management.models import User

from sqlalchemy import UniqueConstraint


class Address(BASE):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    resident_name = Column(String, nullable=True)
    house_number = Column(String, nullable=True)
    street_number = Column(String, nullable=True)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    zipcode = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    added_by = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="addresses")

    __table_args__ = (UniqueConstraint('house_number', 'added_by', name='address_house_no_added_by_uix_1'),)
