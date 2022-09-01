from database import session_db


class DBInternalError(Exception):
    ...


def get_session():
    db = None
    try:
        db = session_db()
        yield db
    finally:
        if db is not None:
            db.close()
