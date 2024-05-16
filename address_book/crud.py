# address_book/crud.py
import logging

from config import get_db, DATABASEERROR, log
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from address_book import schemas
from address_book import models
from starlette.responses import JSONResponse


def get_address(address_id: int, user_id: int, db: Session = None):
    if db is None:
        db = next(get_db())
    return db.query(models.Address).filter(models.Address.id == address_id, models.Address.added_by == user_id).first()


def create_address(address: schemas.AddressCreate, db: Session = None):
    log.info(f'adding new address {address}')
    if db is None:
        db = next(get_db())
    db_address = models.Address(**address.dict())
    try:
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
    except IntegrityError:
        db.rollback()
        raise DATABASEERROR
    db.close()
    return db_address


def update_address(address: schemas.AddressEdit, address_id: int, db: Session = None):
    if db is None:
        db = next(get_db())
    existing_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    added_by = existing_address.added_by
    try:
        for key, value in address.dict().items():
            setattr(existing_address, key, value)
        existing_address.added_by = added_by
        db.commit()
        db.refresh(existing_address)
    except IntegrityError:
        db.rollback()
        return DATABASEERROR
    db.close()
    return existing_address


def delete_address(address_id: int, user_id: int, db: Session = None):
    if db is None:
        db = next(get_db())
    existing_address = db.query(models.Address).filter(models.Address.id == address_id,
                                                       models.Address.added_by == user_id).first()
    if existing_address:
        try:
            db.delete(existing_address)
            db.commit()
        except IntegrityError:
            db.rollback()
            return DATABASEERROR
    else:
        raise HTTPException(status_code=404, detail="no address found in db to delete")
    db.close()
    return JSONResponse(status_code=410, content={'message': 'address deleted successfully'})
