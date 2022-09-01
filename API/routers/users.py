import sys

sys.path.append("../..")

from Models.user_model import User
from fastapi import Depends, APIRouter, Query
from Models import all_models
from Core.database import engin
from sqlalchemy.orm import Session
from pydantic import BaseModel
from Services.user_services import load_all_users, load_user_by_id, persist_user, get_user_by_id, remove_user
from Core.sessionBuilder import get_session
from Services.auth_services import get_current_user, get_user_exception, verify_password, get_hash_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

all_models.Base.metadata.create_all(bind=engin)


# it should go to schema package
class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


@router.get("/")
async def read_all_users(session: Session = Depends(get_session)):
    return load_all_users(session)


@router.get("/user/{user_id}")
async def read_user_by_path(user_id: int, session: Session = Depends(get_session)):
    user_entity = load_user_by_id(user_id, session)

    if user_entity is not None:
        return user_entity

    return "Invalid user_id"


@router.get("/user/")
async def read_user_by_query(user_id: int = Query(default=None), session: Session = Depends(get_session)):
    user_entity = load_user_by_id(user_id, session)

    if user_entity is not None:
        return user_entity

    return "Invalid user_id"


@router.put("/user/password")
async def change_user_password(user_verification: UserVerification,
                               user: dict[str, str] = Depends(get_current_user),
                               session: Session = Depends(get_session)):
    if user is None:
        raise get_user_exception()

    user_entity: User = get_user_by_id(int(user.get("id")), session)

    if user_entity is not None:
        if user_verification.username == user_entity.username and verify_password(
                user_verification.password,
                user_entity.hashed_password):
            user_entity.hashed_password = get_hash_password(user_verification.new_password)
            persist_user(user_entity, session)
            session.commit()
            return "Successful"
    return "Invalid user or request"


@router.delete("/user")
async def delete_user(user: dict[str, str] = Depends(get_current_user),
                      session: Session = Depends(get_session)):
    if user is None:
        raise get_user_exception()

    user_entity: User = get_user_by_id(int(user.get("id")), session)

    if user_entity is None:
        return "Invalid user or request"

    remove_user(int(user.get("id")), session)

    return "Deleted Successfully!"
