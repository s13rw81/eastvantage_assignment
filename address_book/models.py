# address_book/models.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    resident_name = Column(String, index=True)
    house_number = Column(String)
    street_number = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    zipcode = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
