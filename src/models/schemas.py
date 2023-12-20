from pydantic import BaseModel
from pydantic import EmailStr
from typing import List, Optional
from enum import Enum


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass

    class Config:
        orm_mode = True


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class Roles(str, Enum):
    user = "user"
    admin = "admin"


class UserBase(BaseModel):
    email: EmailStr
    role: Roles = "user"


class UserCreate(UserBase):
    password: str


UserAuth = UserCreate


class LiteUser(UserBase):
    id: int


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
