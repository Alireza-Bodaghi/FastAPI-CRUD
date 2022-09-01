import sys

sys.path.append("../..")

from Services.address_services import persist_address
from Services.user_services import load_user_by_id, persist_user
from typing import Optional
from fastapi import APIRouter, Depends
from Models.user_model import User
from Models.address_model import Address
from Models import all_models
from Core.database import engin
from Core.sessionBuilder import get_session
from sqlalchemy.orm import Session
from pydantic import BaseModel
from Services.auth_services import get_current_user, get_user_exception


# in case you didn't use alembic to create
# your database, you should use this line that
# automatically creates your necessary database.
# but right now that we have created the tables by
# alembic, we can comment this line for sure!
all_models.Base.metadata.create_all(bind=engin)

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"],
    responses={404: {"description": "Not found!"}}

)


class AddressSchema(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postalcode: str


@router.post("/")
async def create_address(address: AddressSchema,
                         user: dict[str, str] = Depends(get_current_user),
                         session: Session = Depends(get_session)):
    if user is None:
        raise get_user_exception()

    address_entity = Address()
    address_entity.address1 = address.address1
    address_entity.address2 = address.address2
    address_entity.city = address.city
    address_entity.state = address.state
    address_entity.country = address.country
    address_entity.postalcode = address.postalcode

    persist_address(address_entity, session)

    # flush() is kinda like commit, and it generates
    # corresponding Pk for the entities. for further
    # info, read flush docs in sqlalchemy orm
    session.flush()

    user_entity: User = load_user_by_id(int(user.get("id")), session)
    user_entity.address_id = address_entity.id

    # you can even comment the next line. for further info check sqlalchemy docs.
    persist_user(user_entity, session)

    session.commit()

