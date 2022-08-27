from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    id: UUID
    # data validation by pydantic and Field
    title: str = Field(min_length=1)

    author: str = Field(min_length=1, max_length=100)

    # making description optional (not required)
    # setting a title for documenting purposes
    # setting boundary fot input
    description: Optional[str] = Field(title="Description of the book",
                                       max_length=100,
                                       min_length=1)

    # gt and lt are exclusive,
    # so make sure to put the right value!
    rating: int = Field(gt=-1, lt=101)


BOOKS = []


@app.get("/")
async def get_all_books() -> list[Book]:
    if len(BOOKS) < 1:
        creating_books_not_an_api()
    return BOOKS


@app.post("/")
async def create_book(book: Book) -> Book:
    BOOKS.append(book)
    return book


# this is just a way to have data to manipulate
# we could also use __init__ magic method to construct
# data. there is no deference in the output we're getting.
# this is to get data 'cause we don't have database yet.
def creating_books_not_an_api():
    for i in range(1, 5):
        new_book = Book(id=f"24b0d1e9-452a-41f5-b734-931d0392eed{i}",
                        title=f"title {i}",
                        author=f"author {i}",
                        description=f"description {i}",
                        rating=i)
        BOOKS.append(new_book)
