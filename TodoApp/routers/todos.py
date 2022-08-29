import sys

sys.path.append("..")

from typing import Optional
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import models
from database import engin, session_db
from pydantic import BaseModel, Field
from .auth import get_current_user, get_user_exception

models.Base.metadata.create_all(bind=engin)


# internally configuring router's prefix, tags and responses
router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={
        404: {"description": "Not found!"}
    })


# a dependable function:
def get_db():
    db = None
    try:
        db = session_db()
        yield db
    finally:
        if db is not None:
            db.close()


class TodoModel(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="priority is between 1-5 inclusive")
    is_complete: bool


# using 'Depends()' to inject get_db before path operation
# so this api is called 'dependent' and 'get_db' is called
# 'dependable'
# this is how dependency injection in FastAPI works.
@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()


# getting token on different port(like 9000) from auth.py
# and using that token to retrieve data from another port(like 8000)
# from main.py.
# get_current_user dependency runs before path operations and gets
# a user in the format of dict.
@router.get("/user")
async def read_all_todos_by_user(user: dict[str, str] = Depends(get_current_user),
                                 db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    todos: list[models.Todo] = db.query(models.Todo) \
        .filter(models.Todo.owner_id == user.get("id")) \
        .all()
    return todos


@router.get("/{todo_id}")
async def read_todo(todo_id: int,
                    db: Session = Depends(get_db),
                    user: dict[str, str] = Depends(get_current_user)):
    if user is None:
        raise get_user_exception()

    result = db.query(models.Todo) \
        .filter(models.Todo.id == todo_id) \
        .filter(models.Todo.owner_id == user.get("id")) \
        .first()

    if result is not None:
        return result
    raise http_exception()


@router.post("/")
async def create_todo(todo: TodoModel,
                      user: dict[str, str] = Depends(get_current_user),
                      db: Session = Depends(get_db)) -> dict[str, str]:
    if user is None:
        raise get_user_exception()

    todo_entity = models.Todo()
    todo_entity.title = todo.title
    todo_entity.description = todo.description
    todo_entity.priority = todo.priority
    todo_entity.is_complete = todo.is_complete

    # setting user PK for our instance
    todo_entity.owner_id = user.get("id")

    # save an instance after flush or committing transaction
    db.add(todo_entity)

    # commits transaction
    db.commit()

    return {
        'status_code': '201',
        'transaction': 'Successful'
    }


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int,
                      user: dict[str, str] = Depends(get_current_user),
                      db: Session = Depends(get_db)) -> dict[str, str]:
    if user is None:
        raise get_user_exception()

    todo_entity = db.query(models.Todo) \
        .filter(models.Todo.id == todo_id) \
        .filter(models.Todo.owner_id == user.get("id")) \
        .first()

    if todo_entity is None:
        raise http_exception()

    # deletes data after flush or committing transaction
    db.query(models.Todo).filter(models.Todo.id == todo_id).delete()

    db.commit()

    return {
        'status_code': '200',
        'transaction': 'Successful'
    }


@router.put("/{todo_id}")
async def update_todo(todo_id: int,
                      todo: TodoModel,
                      user: dict[str, str] = Depends(get_current_user),
                      db: Session = Depends(get_db)) -> dict[str, str]:
    if user is None:
        raise get_user_exception()

    todo_entity = db.query(models.Todo) \
        .filter(models.Todo.id == todo_id) \
        .filter(models.Todo.owner_id == user.get("id")) \
        .first()

    if todo_entity is None:
        raise http_exception()

    todo_entity.title = todo.title
    todo_entity.description = todo.description
    todo_entity.priority = todo.priority
    todo_entity.is_complete = todo.is_complete
    # updates an instance after flush or committing transaction by PK
    db.add(todo_entity)
    db.commit()

    return {
        'status_code': '200',
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404,
                         detail="Todo not found!")
