from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from models.model import Item
from models.schemas import ItemCreate, LiteUser


def save(db: Session, item_data: ItemCreate, user_data: LiteUser):
    if db.scalar(select(Item).where(Item.title == item_data.title)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Item with this title already exists!"
        )
    item = Item(title=item_data.title)
    item.description = item_data.description
    item.owner_id = user_data.id
    db.add(item)
    db.commit()
    return {
        "id": item.id,
        "title": item.title,
    }


def delete(db: Session, item_id: int):
    item = db.get(entity=Item, ident=item_id)
    db.delete(item)
    db.commit()

