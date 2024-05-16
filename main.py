from typing import List

from address_book import crud as address_crud
from address_book import schemas as address_schemas
from address_book.models import Address
from address_book.schemas import AddressInDB
from config import ENVIRONMENT, BASE, engine, RANDOM_USERS, get_db
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic
from geopy.distance import geodesic
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from user_management.crud import create_user
from user_management.crud import delete_user
from user_management.schemas import User, UserCreate

app = FastAPI()
# Security
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.on_event("startup")
async def startup_event():
    BASE.metadata.create_all(engine)
    # add 3 random users
    # for user_data in RANDOM_USERS:
    #     create_user(user=user_data)


# homepage
@app.get("/")
async def root():
    msg = "Eastvantage Fast API assignment. Kindly navigate to  the {}/docs to use the API"
    if ENVIRONMENT == 'dev':
        return {"message": msg.format('http://localhost')}
    else:
        return {"message": msg.format('http://0.0.0.0')}


# User APIs
@app.post("/add_user/", response_model=User)
def add_user(user: UserCreate, db=Depends(get_db)):
    return create_user(user, db=db)


@app.delete("/remove_user/", response_model=User)
async def remove_user(user_id: int, db=Depends(get_db)):
    return delete_user(user_id, db=db)


# add a new address
@app.post("/add_address/", response_model=address_schemas.Address)
async def create_address(address: address_schemas.AddressCreate):
    return address_crud.create_address(address=address)


# update an address
@app.put("/update_address/", response_model=address_schemas.Address)
def update_address(changed_address: address_schemas.AddressEdit, db: Session = Depends(get_db)):
    address_id = changed_address.address_id
    user_id = changed_address.user_id
    db_address = address_crud.get_address(address_id=address_id, user_id=user_id, db=db)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found or address does not belong to user.")
    else:
        return address_crud.update_address(db=db, address=changed_address, address_id=address_id)


# delete an address
@app.delete("/delete_address/{address_id}", response_model=address_schemas.Address)
def delete_address(address_id: int, user_id: int, db: Session = Depends(get_db)):
    db_address = address_crud.get_address(address_id=address_id, db=db, user_id=user_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address_crud.delete_address(db=db, user_id=user_id, address_id=address_id)


@app.get("/get_address/{address_id}", response_model=address_schemas.Address)
async def read_address(address_id: int, user_id: int):
    db_address = address_crud.get_address(address_id, user_id=user_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.get("/get_addresses_within_distance/", response_model=List[AddressInDB])
def get_addresses(latitude: float, longitude: float, user_id: int, distance: float, db=Depends(get_db)):
    user_coordinates = (latitude, longitude)
    addresses = db.query(Address).filter(Address.added_by == user_id).all()
    addresses_within_distance = []
    for addr in addresses:
        addr_coordinates = (addr.latitude, addr.longitude)
        if geodesic(user_coordinates, addr_coordinates).kilometers <= distance:
            addresses_within_distance.append(addr)
    # return JSONResponse(content=addresses_within_distance)
    return addresses_within_distance
