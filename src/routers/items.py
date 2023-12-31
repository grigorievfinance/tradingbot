from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated

from src.models import schemas
from src.auth import apikey_scheme
from src.views.items import get_items, get_item_by_id
from src.models.database import get_db
from src.controllers.items import save, delete, update

router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
def read_items(access_token: Annotated[str, Depends(apikey_scheme)], skip: int = 0, limit: int = 100,
               db: Session = Depends(get_db)):
    items = get_items(access_token=access_token, db=db, skip=skip, limit=limit)
    return items


@router.delete("/{item_id}")
def delete_item(access_token: Annotated[str, Depends(apikey_scheme)], item_id: int, db: Session = Depends(get_db)):
    delete(access_token=access_token, db=db, item_id=item_id)


@router.get("/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, access_token: Annotated[str, Depends(apikey_scheme)], db: Session = Depends(get_db)):
    return get_item_by_id(access_token=access_token, item_id=item_id, db=db)


@router.post("", response_model=schemas.Item, status_code=201)
def save_item(access_token: Annotated[str, Depends(apikey_scheme)], item_data: schemas.ItemCreate,
              db: Session = Depends(get_db)):
    return save(access_token=access_token, db=db, item_data=item_data)


@router.put("/{item_id}", response_model=schemas.Item, status_code=201)
def update_item(item_id: int, access_token: Annotated[str, Depends(apikey_scheme)], item_data: schemas.ItemCreate,
                db: Session = Depends(get_db)):
    return update(db=db, item_data=item_data, access_token=access_token, item_id=item_id)
