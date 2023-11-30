from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated

from models import schemas
from auth import apikey_scheme
from views.items import get_items, get_item_by_id
from models.database import get_db
from controllers.items import save

router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_items(db=db, skip=skip, limit=limit)


@router.get("/{item_id}/{access_token}", response_model=schemas.Item)
def read_item(item_id: int, access_token: Annotated[str, Depends(apikey_scheme)], db: Session = Depends(get_db)):
    return get_item_by_id(access_token=access_token, item_id=item_id, db=db)


@router.post("", response_model=schemas.Item, status_code=201)
def save_item(item_data: schemas.ItemCreate, db: Session = Depends(get_db)):
    return save(db=db, item_data=item_data)

