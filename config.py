import logging
import os
import sys
from datetime import datetime

from fastapi.exceptions import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

# DATABASE CONFIGURATION
# SQLALCHEMY_DATABASE_URL = "sqlite:///address_book.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
BASE = declarative_base()

WS_LOG_PATH = os.path.join(os.path.curdir, "logs")  # '.\\logs'

# logging
log = logging.getLogger("foliox_logger")
log.setLevel(logging.DEBUG)
logFormatter = logging.Formatter('%(asctime)s - %(filename)s > %(funcName)s() # %(lineno)d [%(levelname)s] %(message)s')
DATE_FORMAT = "%Y-%m-%d"
TODAY = datetime.now().strftime(DATE_FORMAT)
LOG_FILE = os.path.join(WS_LOG_PATH, f"{TODAY}_logs.log")  # '.\\2023_03_11_10_18_logs.log'
consoleHandler = logging.StreamHandler(stream=sys.stderr)
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)

fileHandler = logging.FileHandler(LOG_FILE)  # '.\\logs/.\\2023_03_11_10_18_logs.log'
fileHandler.setFormatter(logFormatter)
log.addHandler(fileHandler)

# ENVIRONMENT VARIABLES
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'DEV').lower()

# EXCEPTIONS
NOTIMPLEMENTEDERROR = HTTPException(status_code=404, detail="this route has not been implemented yet.")
DATABASEERROR = HTTPException(status_code=500, detail="error creating database entry")


def get_db():
    db = Session(engine)
    try:
        yield db
    except Exception as e:
        log.error(str(e))
    finally:
        db.close()


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
