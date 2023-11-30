from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from models.model import Item
from models.schemas import ItemCreate


def save(db: Session, item_data: ItemCreate):
    if db.scalar(select(Item).where(Item.title == item_data.title)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Item with this title already exists!"
        )
    item = Item(title=item_data.title)
    item.description = item_data.description
    db.add(item)
    db.commit()
    return {
        "id": item.id,
        "title": item.title,
    }
