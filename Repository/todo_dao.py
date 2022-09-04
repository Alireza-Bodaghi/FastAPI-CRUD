from Models.todo_model import Todo
from Core.sessionBuilder import DBInternalError
from sqlalchemy.orm import Session


def get_all_todos(session: Session):
    try:
        todos: list[Todo] = session \
            .query(Todo) \
            .all()
    except Exception as e:
        raise DBInternalError(e)

    return todos


def get_all_user_todos(user_id: int, session: Session):
    return session\
        .query(Todo)\
        .filter(Todo.owner_id == user_id)\
        .all()


def get_todo_by_id_and_user_id(todo_id: int, user_id: int, session: Session):
    return session.query(Todo) \
        .filter(Todo.id == todo_id) \
        .filter(Todo.owner_id == user_id) \
        .first()


def save_todo(todo: Todo, session: Session):
    session.add(todo)


def delete_todo(todo_id: int, session: Session):
    session.query(Todo).filter(Todo.id == todo_id).delete()

