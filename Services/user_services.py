from sqlalchemy.orm import Session

from Models.user_model import User
from Repository.user_dao import get_all_users, get_user_by_id, save_user, delete_user


def load_all_users(session: Session):
    return get_all_users(session)


def load_user_by_id(user_id: int, session: Session):
    return get_user_by_id(user_id, session)


def persist_user(user: User, session: Session) -> None:
    save_user(user, session)


def remove_user(user_id: int, session: Session) -> None:
    delete_user(user_id, session)