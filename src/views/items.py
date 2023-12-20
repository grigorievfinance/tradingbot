from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from src.models.model import Token, Item
from src.views.users import get_lite_user


def get_items(access_token: str, db: Session, skip: int = 0, limit: int = 100):
    user = get_lite_user(access_token=access_token, db=db)
    items = db.query(Item).filter_by(owner_id=user.id).offset(skip).limit(limit).all()
    return items


def get_item_by_id(access_token: str, db: Session, item_id: int):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    user = get_lite_user(access_token=access_token, db=db)
    if db.scalar(select(Item).where(Item.id == item_id)):
        item = db.get(entity=Item, ident=item_id)
        if token:
            if item.owner_id == user.id:
                return item
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="UNAUTHORIZED"
            )
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Item with this id not exists!"
        )
