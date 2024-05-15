# main.py
from address_book import crud as address_crud
from address_book import schemas as address_schemas
from address_book.database import engine as address_engine
from fastapi import FastAPI, HTTPException
from user_management import models
from user_management.database import engine as user_engine, get_db

models.Base.metadata.create_all(bind=address_engine)
models.Base.metadata.create_all(bind=user_engine)

app = FastAPI()


# homepage
@app.get("/")
async def root():
    return {"message": "Hello World"}


# login route
@app.post('login/')
async def login():
    pass


# logout route
@app.post("logout/")
async def root():
    pass


@app.post("/addresses/", response_model=address_schemas.Address)
async def create_address(address: address_schemas.AddressCreate):
    db = get_db()
    return address_crud.create_address(db, address)


@app.get("/addresses/{address_id}", response_model=address_schemas.Address)
async def read_address(address_id: int):
    db = get_db()
    db_address = address_crud.get_address(db, address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address
