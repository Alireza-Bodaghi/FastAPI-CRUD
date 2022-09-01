# from TodoApp.database import Base

from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Core.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password=Column(String)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String)
    address_id = Column(Integer, ForeignKey("address.id"))

    # bidirectional relationship (one-to-many relationship)
    todos = relationship("Todo", back_populates="owner")

    # unidirectional relationship (one-to-one relationship)
    address = relationship("Address", back_populates="user_address")
