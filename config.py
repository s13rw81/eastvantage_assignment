import os

from fastapi.exceptions import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

# DATABASE CONFIGURATION
# SQLALCHEMY_DATABASE_URL = "sqlite:///address_book.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
BASE = declarative_base()


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


# ENVIRONMENT VARIABLES
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'DEV').lower()

# EXCEPTIONS
NOTIMPLEMENTEDERROR = HTTPException(status_code=404, detail="this route has not been implemented yet.")
DATABASEERROR = HTTPException(status_code=500, detail="error creating database entry")

RANDOM_USERS = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "1234567890",
        "username": "johndoe1",
        "email": "johndoe1@example.com",
        "password": "password1",
    },
    {
        "first_name": "Jane",
        "last_name": "Doe",
        "phone": "0987654321",
        "username": "janedoe2",
        "email": "janedoe2@example.com",
        "password": "password2",
    },
    {
        "first_name": "Jim",
        "last_name": "Doe",
        "phone": "1122334455",
        "username": "jimdoe3",
        "email": "jimdoe3@example.com",
        "password": "password3",
    },
]
