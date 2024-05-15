# address_book/schemas.py
from pydantic import BaseModel

class AddressBase(BaseModel):
    resident_name: str
    house_number: str
    street_number: str
    city: str
    state: str
    country: str
    zipcode: str
    latitude: float
    longitude: float

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: int

    class Config:
        orm_mode = True
