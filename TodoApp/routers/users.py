import sys

sys.path.append("..")

from fastapi import Depends, APIRouter, Query
import models
from database import engin, session_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user, get_user_exception, verify_password, get_hash_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engin)


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


def get_db():
    db = None
    try:
        db = session_db()
        yield db
    finally:
        if db is not None:
            db.close()


@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.get("/user/{user_id}")
async def read_user_by_path(user_id: int, db: Session = Depends(get_db)):
    user_entity = db.query(models.User) \
        .filter(models.User.id == user_id) \
        .first()

    if user_entity is not None:
        return user_entity

    return "Invalid user_id"


@router.get("/user/")
async def read_user_by_query(user_id: int = Query(default=None), db: Session = Depends(get_db)):
    user_entity = db.query(models.User) \
        .filter(models.User.id == user_id) \
        .first()

    if user_entity is not None:
        return user_entity

    return "Invalid user_id"


@router.put("/user/password")
async def change_user_password(user_verification: UserVerification,
                               user: dict[str, str] = Depends(get_current_user),
                               session: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    # user_entity = session.query(models.User).filter(models.User.id == user.get("id")).first()
    user_entity: models.User = session.get(models.User, int(user.get("id")))

    if user_entity is not None:
        if user_verification.username == user_entity.username and verify_password(
                user_verification.password,
                user_entity.hashed_password):
            user_entity.hashed_password = get_hash_password(user_verification.new_password)
            session.add(user_entity)
            session.commit()
            return "Successful"
    return "Invalid user or request"
