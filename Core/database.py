from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# sqlite configuration:
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

# engin = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False}
# )

DATABASE_URI = 'postgresql://postgres:13724123@localhost/test_engin'

engin = create_engine(DATABASE_URI)

session_db = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engin
)

Base = declarative_base()
