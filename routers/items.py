from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated

from models import schemas
from views.items import get_items
from models.database import get_db


router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_items(db=db, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=schemas.Item)
def read_item(item_id: int):
    return {"item_id": item_id, "name": "first"}
