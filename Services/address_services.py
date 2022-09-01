from Repository.address_dao import save_address
from Models.address_model import Address
from sqlalchemy.orm import Session


def persist_address(address: Address, session: Session):
    save_address(address, session)
