import re
from typing import Optional

from pydantic import BaseModel, ValidationInfo, field_validator


class AddressBase(BaseModel):
    resident_name: Optional[str]
    house_number: Optional[str]
    street_number: Optional[str]
    city: str
    state: str
    country: str
    zipcode: str
    latitude: float
    longitude: float
    added_by: int

    @field_validator('resident_name')
    def validate_resident_name(cls, v: str, info: ValidationInfo) -> str:
        x = v.replace(' ', '')
        if not x.isalpha():
            raise ValueError('Resident name must contain only alphabets')
        return v.title()

    @field_validator('house_number', 'street_number')
    def validate_numbers(cls, v: str, info: ValidationInfo) -> str:
        if not v.isdigit():
            raise ValueError('House and Street numbers must be digits')
        return v

    @field_validator('city', 'state', 'country')
    def validate_location(cls, v: str, info: ValidationInfo) -> str:
        x = v.replace(' ', '')
        if not x.isalpha():
            raise ValueError('City, State, and Country must contain only alphabets')
        return v.title()

    @field_validator('zipcode')
    def validate_zipcode(cls, v: str, info: ValidationInfo) -> str:
        if not re.match(r'^\d{5}$', v):
            raise ValueError('Zipcode must be a 5 digit number')
        return v

    @field_validator('latitude', 'longitude')
    def validate_coordinates(cls, v: float, info: ValidationInfo) -> float:
        if not -90 <= v <= 90:
            raise ValueError('Latitude and Longitude must be between -90 and 90')
        return v

    @field_validator('added_by')
    def validate_added_by(cls, v: int, info: ValidationInfo) -> int:
        if not isinstance(v, int):
            raise ValueError('Added by must be an integer')
        return v


class AddressCreate(AddressBase):
    pass


class AddressEdit(AddressBase):
    resident_name: Optional[str]
    house_number: Optional[str]
    street_number: Optional[str]
    city: str
    state: str
    country: str
    zipcode: str
    latitude: float
    longitude: float
    user_id: int
    address_id: int


class Address(AddressBase):
    id: int


class AddressInDB(AddressBase):
    id: int
