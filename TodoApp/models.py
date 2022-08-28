# from TodoApp.database import Base

from sqlalchemy import Column, Boolean, Integer, String
from database import Base


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    iscomplete = Column(Boolean, default=False)
