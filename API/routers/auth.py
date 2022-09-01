import sys

sys.path.append("../..")

from Core.database import engin
from Services.auth_services import get_hash_password, authenticate_user, create_access_token, get_token_exception
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from Models import all_models
from Models.user_model import User
from datetime import timedelta
from Core.sessionBuilder import get_session

# declaring auth as a router
# router = APIRouter(
#     prefix="/auth",
#     tags=["auth"],
#     responses={
#         401: {"user": "Not Authorized"}
#     }
# )


all_models.Base.metadata.create_all(bind=engin)

# Attention: if you want to use swagger Authorization,
# you have to declare /token API without prefix.
router = APIRouter()


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


@router.post("/create/user")
async def create_new_user(new_user: CreateUser, db: Session = Depends(get_session)):
    user_entity = User()
    user_entity.username = new_user.username
    user_entity.email = new_user.email
    user_entity.first_name = new_user.first_name
    user_entity.last_name = new_user.last_name
    user_entity.hashed_password = get_hash_password(new_user.password)
    user_entity.is_active = True

    db.add(user_entity)
    db.commit()


# read OAuth2PasswordRequestForm docs for further information
# it's a simple form to get username and password
@router.post("/token")
async def login_for_access_token(form: OAuth2PasswordRequestForm = Depends(),
                                 session: Session = Depends(get_session)):
    username = form.username
    password = form.password

    user = authenticate_user(username, password, session)

    if not user:
        raise get_token_exception()

    # defining an expiration time of token
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username,
                                user.id,
                                expires_delta=token_expires)
    # this returns our token. you can get token and paste it
    # in jwt.io to see its content
    return {"token": token}

# Exceptions:
