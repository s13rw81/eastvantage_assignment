from typing import List

from address_book import crud as address_crud
from address_book import schemas as address_schemas
from address_book.models import Address
from address_book.schemas import AddressInDB
from config import ENVIRONMENT, BASE, engine, get_db
from config import log
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic
from geopy.distance import geodesic
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from user_management.crud import create_user
from user_management.crud import delete_user
from user_management.schemas import User, UserCreate

app = FastAPI()
# Security
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.on_event("startup")
async def startup_event():
    log.info(f'starting eastvantage assignment application| running on {ENVIRONMENT} environment')
    BASE.metadata.create_all(engine)
    log.info('all database tables created.')
    # add 3 random users
    # for user_data in RANDOM_USERS:
    #     create_user(user=user_data)


# homepage
@app.get("/", description="This is the root API endpoint. It returns a welcome message.")
async def root():
    """
    This is the root API endpoint. It returns a welcome message.
    """
    log.info(f'inside index route')
    msg = "Eastvantage Fast API assignment. Kindly navigate to  the {}/docs to use the API"
    if ENVIRONMENT == 'dev':
        return {"message": msg.format('http://localhost')}
    else:
        return {"message": msg.format('http://0.0.0.0')}


# User APIs
@app.post("/add_user/", response_model=User, description='add a new user to the database.')
def add_user(user: UserCreate, db=Depends(get_db)):
    """
    add a new user to the database
    input:
    - **first_name**: The first name of the user.
    - **last_name**: The last name of the user.
    - **phone**: The phone number of the user.
    - **username**: The username of the user.
    - **email**: The email address of the user.
    - **password**: The password for the user.
    output:
    The function will return the details of the newly created user.
    """
    log.info('inside add user route')
    return create_user(user, db=db)


@app.delete("/remove_user/", response_model=User, description='remove a user from the database.')
async def remove_user(user_id: int, db=Depends(get_db)):
    """
    Remove a user from the database.
    input
    - **user_id**: The ID of the user to be removed.

    The function will return the details of the removed user.
    """
    log.info('inside delete user route')
    return delete_user(user_id, db=db)


# add a new address
@app.post("/add_address/", response_model=address_schemas.Address, description="Add a new address to the database.")
async def create_address(address: address_schemas.AddressCreate):
    """
    Add a new address to the database.
    input:
    - **resident_name**: The resident's name (optional).
    - **house_number**: The house number (optional).
    - **street_number**: The street number (optional).
    - **city**: The city.
    - **state**: The state.
    - **country**: The country.
    - **zipcode**: The zipcode.
    - **latitude**: The latitude.
    - **longitude**: The longitude.
    - **added_by**: The ID of the user who added the address.
    output:
    The function will return the details of the newly created address.
    """
    log.info('inside create add route')
    return address_crud.create_address(address=address)


# update an address
@app.put("/update_address/", response_model=address_schemas.Address, description='update an existing address in the database.')
def update_address(changed_address: address_schemas.AddressEdit, db: Session = Depends(get_db)):
    """
    Update an existing address in the database.
    input:
    - **changed_address**: The updated address details.
    - **db**: The database session.
    output:
    The function will return the details of the updated address. If the address is not found or does not belong to the user, it will raise an HTTP 404 error.
    """
    log.info('inside update address route')
    address_id = changed_address.address_id
    user_id = changed_address.user_id
    db_address = address_crud.get_address(address_id=address_id, user_id=user_id, db=db)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found or address does not belong to user.")
    else:
        return address_crud.update_address(db=db, address=changed_address, address_id=address_id)


# delete an address
@app.delete("/delete_address/{address_id}", response_model=address_schemas.Address, description='remove an address from the database.')
def delete_address(address_id: int, user_id: int, db: Session = Depends(get_db)):

    log.info('inside delete address route')
    db_address = address_crud.get_address(address_id=address_id, db=db, user_id=user_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address_crud.delete_address(db=db, user_id=user_id, address_id=address_id)


@app.get("/get_address/{address_id}", response_model=address_schemas.Address)
async def read_address(address_id: int, user_id: int):
    log.info('inside get address route')
    db_address = address_crud.get_address(address_id, user_id=user_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.get("/get_addresses_within_distance/", response_model=List[AddressInDB], description='return a list of address belongint to user_id which are withing the specified distance of the latitude and longitude mentioned.')
def get_addresses(latitude: float, longitude: float, user_id: int, distance: float, db=Depends(get_db)):
    """
    This function returns a list of addresses within a specified distance from a given latitude and longitude.
    input:
    latitude (float): The latitude of the user's location.
    longitude (float): The longitude of the user's location.
    user_id (int): The ID of the user.
    distance (float): The distance within which to find addresses.
    db (Session, optional): The database session. Defaults to Depends(get_db).
    output:
    List[AddressInDB]: A list of addresses within the specified distance.
    """
    log.info('inside get_addresses_within_distance route')
    user_coordinates = (latitude, longitude)
    addresses = db.query(Address).filter(Address.added_by == user_id).all()
    addresses_within_distance = []
    for addr in addresses:
        addr_coordinates = (addr.latitude, addr.longitude)
        if geodesic(user_coordinates, addr_coordinates).kilometers <= distance:
            addresses_within_distance.append(addr)
    return addresses_within_distance
