from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Core.database import Base


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
