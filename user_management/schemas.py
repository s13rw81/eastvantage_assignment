# user_management/schemas.py
from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
