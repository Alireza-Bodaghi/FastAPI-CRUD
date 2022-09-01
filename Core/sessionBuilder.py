from sqlalchemy.exc import SQLAlchemyError

from Core.database import session_db


class DBInternalError(Exception):
    ...


def get_session():
    session = None
    try:
        session = session_db()
        yield session

    except SQLAlchemyError as e:
        # logger.error(e.args)
        print(e)
        session.rollback()
    finally:
        if session is not None:
            session.close()
