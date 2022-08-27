from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    id: UUID
    # data validation by pydantic and Field
    title: str = Field(min_length=1)

    author: str

    # making description optional (not required)
    # setting a title for documenting purposes
    # setting boundary fot input
    description: Optional[str] = Field(title="Description of the book",
                                       max_length=100,
                                       min_length=1)

    rating: int


BOOKS = []


@app.get("/")
async def get_all_books() -> list[Book]:
    return BOOKS


@app.post("/")
async def create_book(book: Book) -> Book:
    BOOKS.append(book)
    return book
