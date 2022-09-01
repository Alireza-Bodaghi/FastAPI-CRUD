import sys
from typing import Optional

from fastapi import Depends, HTTPException
from starlette import status

sys.path.append("..")

from sqlalchemy.orm import Session
from Models.user_model import User
from passlib.context import CryptContext
from Models import all_models
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from Core.database import engin

# this is secret key of jwt signature
SECRET_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJ"

# alg in jwt header
ALGORITHM = "HS256"

# pip install "passlib[bcrypt]"
# by installing module, we can encrypt our passwords
# hash! apparently it's a popular library for encrypting.
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

all_models.Base.metadata.create_all(bind=engin)

oath2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def get_hash_password(password: str):
    return bcrypt_context.hash(password)


# verifying password by bcrypt.verify method
def verify_password(plain_password: str, hashed_password: str):
    return bcrypt_context.verify(plain_password, hashed_password)


# authenticating user
def authenticate_user(username: str, password: str, db: Session):
    user: User = db.query(User) \
        .filter(User.username == username) \
        .first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str,
                        user_id: int,
                        expires_delta: Optional[timedelta]):
    # subject claim in payload
    encode = {"sub": username, "id": user_id}

    # expire time:
    if expires_delta:
        # if expiration time is passed through method, then use it
        # and if not, define a default expiration time, like 15 minuts
        # using datetime.utcnow() will avoid local time differences.
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # update method of dictionary can either get a dict
    # or get a key/value iterable.
    # if key exits, update the value of the dict that invoked update from second dict,
    # if key/keys of second do/does not match the first one, adds them to it.
    encode.update({'exp': expire})

    # creating a real jwt token:
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# decoding token and getting username and user_id(PK)
async def get_current_user(token: str = Depends(oath2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username: str = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {
            "username": username,
            "id": user_id
        }
    except JWTError:
        raise get_user_exception()


def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials!",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return credentials_exception


def get_token_exception():
    token_exception_response = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Incorrect username or password",
                                             headers={"WWW-Authenticate": "Bearer"})
    return token_exception_response
