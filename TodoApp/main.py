# from TodoApp import models
# from TodoApp.database import engin

from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engin, session_db
from pydantic import BaseModel, Field

app = FastAPI()

models.Base.metadata.create_all(bind=engin)


# a dependable function:
def get_db():
    try:
        db = session_db()
        yield db
    finally:
        db.close()


class TodoModel(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="priority is between 1-5 inclusive")
    iscomplete: bool


# using 'Depends()' to inject get_db before path operation
# so this api is called 'dependent' and 'get_db' is called
# 'dependable'
# this is how dependency injection in FastAPI works.
@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    result = db.query(models.Todo) \
        .filter(models.Todo.id == todo_id) \
        .first()

    if result is not None:
        return result
    raise http_exception()


@app.post("/")
async def create_todo(todo: TodoModel, db: Session = Depends(get_db)) -> dict[str, str]:
    todo_entity = models.Todo()
    todo_entity.title = todo.title
    todo_entity.description = todo.description
    todo_entity.priority = todo.priority
    todo_entity.iscomplete = todo.iscomplete
    # save an instance after flush or committing transaction
    db.add(todo_entity)
    # commits transaction
    db.commit()

    return {
        'status_code': '201',
        'transaction': 'Successful'
    }


@app.put("/{todo_id}")
async def create_todo(todo_id: int, todo: TodoModel, db: Session = Depends(get_db)) -> dict[str, str]:
    todo_entity = db.query(models.Todo) \
        .filter(models.Todo.id == todo_id) \
        .first()

    if todo_entity is None:
        raise http_exception()

    todo_entity.title = todo.title
    todo_entity.description = todo.description
    todo_entity.priority = todo.priority
    todo_entity.iscomplete = todo.iscomplete
    # updates an instance after flush or committing transaction by PK
    db.add(todo_entity)
    db.commit()

    return {
        'status_code': '200',
        'transaction': 'Successful'
    }


@app.delete("/{todo_id}")
async def create_todo(todo_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    todo_entity = db.query(models.Todo) \
        .filter(models.Todo.id == todo_id) \
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


def http_exception():
    return HTTPException(status_code=404,
                         detail="Todo not found!")
