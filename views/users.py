from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from models import model
from models.model import Token, User
from models.schemas import LiteUser


def get_users(access_token: str, db: Session, skip: int = 0, limit: int = 100):
    user = get_user(access_token=access_token, db=db)
    if user.role == "admin":
        return db.query(model.User).offset(skip).limit(limit).all()
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="You must be ADMIN"
        )


def get_lite_user(access_token: str, db: Session):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    user = LiteUser(id=token.user.id, email=token.user.email)
    if token:
        return user
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )


def get_user(access_token: str, db: Session):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        return get_user_by_id(db=db, user_id=token.user.id)
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )


def get_user_by_id(db: Session, user_id: int):
    if db.scalar(select(User).where(User.id == user_id)):
        user = db.get(entity=User, ident=user_id)
        return user
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this id not exists!"
        )
