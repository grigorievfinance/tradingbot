from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from models.model import User
from models.schemas import UserCreate, Roles
from auth import pwd_context
from views.users import get_user, get_user_by_id


def register_user(db: Session, user_data: UserCreate):
    if db.scalar(select(User).where(User.email == user_data.email)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this email already exists!"
        )
    user = User(email=user_data.email, role="user")
    user.hashed_password = pwd_context.hash(user_data.password)
    db.add(user)
    db.commit()
    return {
        "id": user.id,
        "email": user.email,
    }


def update_user(access_token: str, db: Session, user_data: UserCreate):
    if db.scalar(select(User).where(User.email == user_data.email)):
        user = get_user(access_token=access_token, db=db)
        db.query(User).filter_by(id=user.id).update(
            {
                "email": user_data.email,
                # "role": user_data.role,
                "hashed_password": pwd_context.hash(user_data.password)
            }
        )
        db.commit()
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this email not exists!"
        )


def delete_user(access_token: str, db: Session, user_id: int):
    user = get_user(access_token=access_token, db=db)
    if user.role == Roles.admin:
        del_user = get_user_by_id(db=db, user_id=user_id)
        db.delete(del_user)
        db.commit()
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="You must be ADMIN"
        )