# from TodoApp.database import Base

from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password=Column(String)
    is_active = Column(Boolean, default=True)
    # bidirectional relationship
    todos = relationship("Todo", back_populates="owner")


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    is_complete = Column(Boolean, default=False)
    # defining a foreign key to user
    owner_id = Column(Integer, ForeignKey("user.id"))
    # bidirectional relationship
    owner = relationship("User", back_populates="todos")
