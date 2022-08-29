import sys
sys.path.append("..")

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import session_db, engin
import models
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError


# this is secret key of jwt signature
SECRET_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJ"

# alg in jwt header
ALGORITHM = "HS256"

models.Base.metadata.create_all(bind=engin)

oath2_bearer = OAuth2PasswordBearer(tokenUrl="token")

# declaring auth as a router
router = APIRouter()


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


@router.post("/create/user")
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
@router.post("/token")
async def login_for_access_token(form: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    username = form.username
    password = form.password

    user = authenticate_user(username, password, db)

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
def get_user_exception():
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials!",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return credentials_exception


def get_token_exception():
    token_exception_response = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Incorrect username or password",
                                             headers={"WWW-Authenticate": "Bearer"})
    return token_exception_response
