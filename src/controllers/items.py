from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from src.models.model import Item
from src.models.schemas import ItemCreate
from src.views.users import get_lite_user


def save(access_token: str, db: Session, item_data: ItemCreate):
    user = get_lite_user(access_token=access_token, db=db)
    if db.scalar(select(Item).where(Item.title == item_data.title)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Item with this title already exists!"
        )
    item = Item(title=item_data.title)
    item.description = item_data.description
    item.owner_id = user.id
    db.add(item)
    db.commit()
    return item


def update(access_token: str, db: Session, item_data: ItemCreate, item_id: int):
    if db.scalar(select(Item).where(Item.id == item_id)):
        user = get_lite_user(access_token=access_token, db=db)
        item = db.get(entity=Item, ident=item_id)
        if item.owner_id == user.id:
            db.query(Item).filter_by(id=item_id).update(
                {
                    "title": item_data.title,
                    "description": item_data.description
                }
            )
            db.commit()
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="UNAUTHORIZED"
            )
        return item
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Item with this id not exists!"
        )


def delete(access_token: str, db: Session, item_id: int):
    if db.scalar(select(Item).where(Item.id == item_id)):
        user = get_lite_user(access_token=access_token, db=db)
        item = db.get(entity=Item, ident=item_id)
        if item.owner_id == user.id:
            db.delete(item)
            db.commit()
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



