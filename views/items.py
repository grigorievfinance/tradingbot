from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from models import model
from models.model import Token


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Item).offset(skip).limit(limit).all()


def get_item_by_id(access_token: str, db: Session, item_id: int):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        item = db.get(entity=model.Item, ident=item_id)
        return item
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )
