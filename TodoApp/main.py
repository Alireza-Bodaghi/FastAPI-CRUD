# from TodoApp import models
# from TodoApp.database import engin

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engin, session_db

app = FastAPI()

models.Base.metadata.create_all(bind=engin)


# a dependable functions
def get_db():
    try:
        db = session_db()
        yield db
    finally:
        db.close()


# using Depends to inject get_db before path operation
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


def http_exception():
    return HTTPException(status_code=404,
                        detail="Todo not found!")