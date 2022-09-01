from Models.address_model import Address
from sqlalchemy.orm import Session


def save_address(address: Address, session: Session) -> None:
    session.add(address)
