from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import session_db, engin
from passlib.context import CryptContext
import models


models.Base.metadata.create_all(bind=engin)

app = FastAPI()


def get_db():
    db = None
    try:
        db = session_db()
        yield db
    finally:
        if db is not None:
            db.close()


# pip install "passlib[bcrypt]"
# by installing module, we can encrypt our passwords
# hash! apparently it's a popular library for encrypting.
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


def get_hash_password(password: str):
    return bcrypt_context.hash(password)


# verifying password by bcrypt.verify method
def verify_password(plain_password: str, hashed_password: str):
    return bcrypt_context.verify(plain_password, hashed_password)


# authenticating user
def authenticate_user(username: str, password: str, db: Session):
    user: models.User = db.query(models.User)\
        .filter(models.User.username == username)\
        .first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@app.post("/create/user")
async def create_new_user(new_user: CreateUser, db: Session = Depends(get_db)):
    user_entity = models.User()
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
@app.post("/token")
async def login_for_access_token(form: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    username = form.username
    password = form.password

    user = authenticate_user(username, password, db)

    if not user:
        raise HTTPException(status_code=404,
                            detail="user not found!")
    return "user verified"
