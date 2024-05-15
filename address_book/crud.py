# address_book/crud.py
from sqlalchemy.orm import Session
from address_book import schemas

from . import models


def get_address(db: Session, address_id: int):
    return db.query(models.Address).filter(models.Address.id == address_id).first()


def create_address(db: Session, address: schemas.AddressCreate):
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address
