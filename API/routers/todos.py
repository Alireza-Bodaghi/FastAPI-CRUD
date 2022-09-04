import json
import sys
import traceback

sys.path.append("../..")

from Models.todo_model import Todo
from typing import Optional
from fastapi import Depends, HTTPException, APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from Models import all_models
from Core.database import engin
from Core.sessionBuilder import get_session
from Services.todo_services import load_all_todos, load_all_user_todos, load_todo_by_id_and_user_id, persist_todo, \
    remove_todo
from pydantic import BaseModel, Field
from Services.auth_services import get_current_user, get_user_exception, get_current_user_by_header_auth

all_models.Base.metadata.create_all(bind=engin)

# internally configuring router's prefix, tags and responses
router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={
        404: {"description": "Not found!"}
    })


class TodoModel(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="priority is between 1-5 inclusive")
    is_complete: bool


# using 'Depends()' to inject get_db before path operation
# so this API is called 'dependent' and 'get_db' is called
# 'dependable'
# this is how dependency injection in FastAPI works.
@router.get("/")
async def read_all(session: Session = Depends(get_session)):
    return load_all_todos(session)


# getting token on different port(like 9000) from auth.py
# and using that token to retrieve data from another port(like 8000)
# from main.py.
# get_current_user dependency runs before path operations and gets
# a user in the format of dict.
@router.get("/user")
async def read_all_todos_by_user(user: dict[str, str] = Depends(get_current_user),
                                 session: Session = Depends(get_session)):
    if user is None:
        raise get_user_exception()

    todos: list[Todo] = load_all_user_todos(int(user.get("id")), session)
    return todos


@router.get("/{todo_id}")
async def read_todo(todo_id: int,
                    session: Session = Depends(get_session),
                    user: dict[str, str] = Depends(get_current_user)):
    if user is None:
        raise get_user_exception()

    result = load_todo_by_id_and_user_id(int(todo_id), int(user.get("id")), session)

    if result is not None:
        return result
    raise http_exception()


@router.post("/")
async def create_todo(todo: TodoModel,
                      user: dict[str, str] = Depends(get_current_user),
                      session: Session = Depends(get_session)) -> dict[str, str]:
    if user is None:
        raise get_user_exception()

    todo_entity = Todo()
    todo_entity.title = todo.title
    todo_entity.description = todo.description
    todo_entity.priority = todo.priority
    todo_entity.is_complete = todo.is_complete

    # setting user PK for our instance
    todo_entity.owner_id = user.get("id")

    # save an instance after flush or committing transaction
    # db.add(todo_entity)
    persist_todo(todo_entity, session)
    # commits transaction
    session.commit()

    return {
        'status_code': '201',
        'transaction': 'Successful'
    }


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int,
                      user: dict[str, str] = Depends(get_current_user),
                      session: Session = Depends(get_session)) -> dict[str, str]:
    if user is None:
        raise get_user_exception()

    todo_entity = load_todo_by_id_and_user_id(todo_id, int(user.get("id")), session)

    if todo_entity is None:
        raise http_exception()

    # deletes data after flush or committing transaction
    remove_todo(todo_id, session)
    session.commit()

    return {
        'status_code': '200',
        'transaction': 'Successful'
    }


@router.put("/{todo_id}")
async def update_todo(todo_id: int,
                      todo: TodoModel,
                      user: dict[str, str] = Depends(get_current_user),
                      session: Session = Depends(get_session)) -> dict[str, str]:
    if user is None:
        raise get_user_exception()

    todo_entity = load_todo_by_id_and_user_id(todo_id, int(user.get("id")), session)

    if todo_entity is None:
        raise http_exception()

    todo_entity.title = todo.title
    todo_entity.description = todo.description
    todo_entity.priority = todo.priority
    todo_entity.is_complete = todo.is_complete
    # updates an instance after flush or committing transaction by PK
    persist_todo(todo_entity, session)
    session.commit()

    return {
        'status_code': '200',
        'transaction': 'Successful'
    }


@router.websocket("/websocket/create/")
async def websocket_endpoint(websocket: WebSocket,
                             session: Session = Depends(get_session),
                             user: dict[str, str] = Depends(get_current_user_by_header_auth)):
    try:
        await websocket.accept()
        print(user)

        while True:
            request_text = await websocket.receive_json()
            request_json = json.dumps(request_text)
            data_dict = json.loads(request_json)
            todo: Todo = Todo()
            todo.title = str(data_dict['title'])
            todo.priority = int(data_dict['priority'])
            todo.description = str(data_dict['description'])
            todo.is_complete = bool(data_dict['is_complete'])
            todo.owner_id = user.get("id")
            persist_todo(todo, session)
            session.commit()
            await websocket.send_json(request_json)

    except WebSocketDisconnect as e:
        print("client has closed the connections")
        traceback.print_exception(*sys.exc_info())
        session.rollback()

    except Exception as e:
        print("an exception occurred")
        traceback.print_exception(*sys.exc_info())
        session.rollback()

def http_exception():
    return HTTPException(status_code=404,
                         detail="Todo not found!")
