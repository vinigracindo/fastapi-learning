from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book",
                                       max_length=100,
                                       min_length=1)
    rating: int = Field(gt=-1, lt=101)


BOOKS = []


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise raise_item_cannot_be_found_exception()


@app.get("/")
async def read_all_books():
    if len(BOOKS) < 1:
        create_books_no_api()
    return BOOKS


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    for index, item in enumerate(BOOKS):
        if item.id == book_id:
            BOOKS[index] = book
            return book
    raise raise_item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            del BOOKS[index]
            return f'ID: {book_id} deleted.'
    raise raise_item_cannot_be_found_exception()


def create_books_no_api():
    book_1 = Book(id="b87b6ccc-30c0-45be-99c7-f57f5a5d4353",
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=60)
    book_2 = Book(id="b17b6ccc-30c0-45be-99c7-f57f5a5d4353",
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=70)
    book_3 = Book(id="b27b6ccc-30c0-45be-99c7-f57f5a5d4353",
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=80)
    book_4 = Book(id="b37b6ccc-30c0-45be-99c7-f57f5a5d4353",
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=92)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404, detail="Book not found",
                         headers={"X-Header-Error": "Nothing to be seen at the UUID."})