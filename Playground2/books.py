from typing import Optional

from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse
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

# to provide an example of your schema you define a class named 'Config'
# and then you should assign an example value of your value to the property
# named 'schema_extra'. these values will show on swagger UI.
# attention: 'Config' and 'schema_extra' are not just arbitrary names!
# so keep in mind that must use the same names!
    class Config:
        schema_extra = {
            "example": {
                "id": "24b0d1e9-452a-41f5-b734-931d0392eed1",
                "title": "a title for book",
                "author": "author full name if possible",
                "description": "a description for describing the content of book",
                "rating": 20
            }
        }


# using another model with no rating property as respons model
# in our apis. for example, we have class of user that has
# user_name and password. in response we would like to return an object
# that has no password property! this way we can handle that scenario.
class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book",
                                       max_length=100,
                                       min_length=1)


# custom exceptions and using it in fastAPI exception handler
class NegativeNumException(Exception):
    def __init__(self, number_of_books_to_return: int):
        self.number_of_books_to_return = number_of_books_to_return


BOOKS = []


# exception handler of fastAPI to handle exception in a way that you
# prefer. pay attention to the argument of method!
@app.exception_handler(NegativeNumException)
async def negative_number_exception_handler(request: Request, exception: NegativeNumException):
    # content field must be dict to proceed
    return JSONResponse(
        status_code=418,
        content={"message": f"Are you out of your mind?"
                 f" trying to get {exception.number_of_books_to_return} books? "
                 f"please try again with valid number!"}
    )


@app.get("/")
async def get_all_books(number_of_books_to_return: Optional[int] = None) -> list[Book]:
    if number_of_books_to_return and number_of_books_to_return < 0:
        raise NegativeNumException(number_of_books_to_return)

    if len(BOOKS) < 1:
        creating_books_not_an_api()

    if number_of_books_to_return and len(BOOKS) > number_of_books_to_return > 0:
        new_books = []
        for i in range(number_of_books_to_return):
            new_books.append(BOOKS[i])
        return new_books
    return BOOKS


# get specific book by unique uuid
@app.get("/book/{book_id}")
async def get_book_by_uuid(book_id: UUID) -> Book:
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise item_not_found()


@app.get("/book/rating/{book_id}",response_model=BookNoRating)
async def get_book_by_uuid(book_id: UUID) -> Book:
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise item_not_found()


# by using status_code in path parameter we can
# attach our specific http code.
@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book) -> Book:
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book) -> Book:
    index = 0
    for book_itr in BOOKS:
        if book_itr.id == book_id:
            BOOKS[index] = book
            return BOOKS[index]
        index += 1
    raise item_not_found()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID) -> str:
    index = 0
    for book_itr in BOOKS:
        if book_itr.id == book_id:
            del BOOKS[index]
            return f"book with id = {book_id} has been deleted!"
        index += 1
    raise item_not_found()


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


# declaring a function for a specific Exception to raise
# as you can see, we can also declare http header in exception
def item_not_found() -> HTTPException:
    return HTTPException(status_code=404,
                         detail="Book not found",
                         headers={"X-Header-Error": "can't find any book by UUID"})