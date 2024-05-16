from config import get_db, log
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from user_management import models
from user_management import schemas


def create_user(user: schemas.UserCreate, db: Session = None):
    log.info(f"user schema = {user}")
    if db is None:
        db = next(get_db())
    if isinstance(user, dict):
        db_user = models.User(**user)
    else:
        db_user = models.User(**user.dict())
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        log.info(f'create user succeeded. new user is {db_user}')
    except IntegrityError as e:
        log.error(f'error creating user {e}')
        db.rollback()
        raise HTTPException(status_code=409, detail=str(e))
    db.close()
    return db_user


def delete_user(user_id: int, db: Session = None) -> JSONResponse:
    log.info(f'delete user {user_id}')
    if db is None:
        db = next(get_db())
    user = db.query(models.User).filter(models.User.id == user_id).first()
    log.info(f'user found : {user}')
    if user:
        try:
            db.delete(user)
            db.commit()
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=409, detail=str(e))
    else:
        log.error(f'user with {user_id} not found')
        raise HTTPException(status_code=404, detail='user not found.')
    db.close()
    log.info(f'user with id {user_id} deleted.')
    return JSONResponse(status_code=410, content={'message': 'user deleted successfully'})
