from Models.user_model import User
from Core.sessionBuilder import DBInternalError
from sqlalchemy.orm import Session


def get_user_by_id(user_id: int,
                   session: Session
                   ) -> User:
    try:
        user_model: User = session \
            .get(User, user_id)

    except Exception as ex:
        raise DBInternalError(ex)

    return user_model


def get_last_users_by_limit(limit_number: int,
                            session: Session
                            ) -> list[User]:
    try:
        users: list[User] = session \
            .query(User) \
            .order_by(User.id.desc()) \
            .limit(limit_number) \
            .all()

    except Exception as ex:
        raise DBInternalError(ex)

    return users


def get_all_users(session: Session) -> list[User]:
    try:
        users: list[User] = session \
            .query(User) \
            .all()

    except Exception as ex:
        raise DBInternalError(ex)

    return users


def save_user(user: User, session: Session) -> None:
    session.add(user)


def delete_user(user_id: int, session: Session) -> None:
    session.query(User).filter(User.id == user_id).delete()
