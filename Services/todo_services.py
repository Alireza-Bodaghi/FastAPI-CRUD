from sqlalchemy.orm import Session

import Models
from Repository.todo_dao import get_all_todos


def get_todos(session: Session):
    return get_all_todos(session)
