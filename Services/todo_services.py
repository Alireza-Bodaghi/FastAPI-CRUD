from sqlalchemy.orm import Session
from Models.todo_model import Todo
from Repository.todo_dao import get_all_todos, get_all_user_todos, get_todo_by_id_and_user_id, save_todo, delete_todo


def load_all_todos(session: Session):
    return get_all_todos(session)


def load_all_user_todos(user_id: int, session: Session):
    return get_all_user_todos(user_id, session)


def load_todo_by_id_and_user_id(todo_id: int, user_id: int, session: Session):
    return get_todo_by_id_and_user_id(todo_id, user_id, session)


def persist_todo(todo: Todo, session: Session):
    save_todo(todo, session)


def remove_todo(todo_id: int, session: Session):
    delete_todo(todo_id, session)