import sys

sys.path.append("..")

from typing import Optional
from fastapi import APIRouter, Depends
import models
from database import engin, session_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user, get_user_exception


# in case you didn't use alembic to create
# your database, you should use this line that
# automatically creates your necessary database.
# but right now that we have created the tables by
# alembic, we can comment this line for sure!
models.Base.metadata.create_all(bind=engin)

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"],
    responses={404: {"description": "Not found!"}}

)


def get_db():
    db = None
    try:
        db = session_db()
        yield db
    finally:
        if db is not None:
            db.close()


class Address(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postalcode: str


@router.post("/")
async def create_address(address: Address,
                         user: dict[str, str] = Depends(get_current_user),
                         session: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    address_entity = models.Address()
    address_entity.address1 = address.address1
    address_entity.address2 = address.address2
    address_entity.city = address.city
    address_entity.state = address.state
    address_entity.country = address.country
    address_entity.postalcode = address.postalcode

    session.add(address_entity)

    # flush() is kinda like commit, and it generates
    # corresponding Pk for the entities. for further
    # info, read flush docs in sqlalchemy orm
    session.flush()

    user_entity: models.User = session.get(models.User, user.get("id"))
    user_entity.address_id = address_entity.id

    session.commit()

