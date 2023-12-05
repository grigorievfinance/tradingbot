from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from models import model
from models.model import Token
from models.schemas import LiteUser


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()


def get_user(access_token: str, db: Session):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    user = LiteUser(id=token.user.id, email=token.user.email)
    if token:
        # return {
        #     "id": token.user.id,
        #     "email": token.user.email
        # }
        return user
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )
