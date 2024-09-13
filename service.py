from typing import List
from pydantic import TypeAdapter
from model import Book, Chapter

from tinydb import Query, TinyDB

db = TinyDB("db.json")


def add_chapter(chapter: Chapter) -> None:
    chapters = db.table("chapters")

    Chapter = Query()
    chapters.remove(Chapter.number == chapter.number)

    chapters.insert(chapter.model_dump())


def get_chapter(book_id: str, number: int) -> Chapter:
    chapters = db.table("chapters")

    Chapter = Query()
    return chapters.get((Chapter.book_id == book_id) & (Chapter.number == number))  # type: ignore


def list_books():
    books = db.table("books")
    listed = books.all()

    return TypeAdapter(type=List[Book]).validate_python(listed)


def list_chapters(book_id: str):
    chapters = db.table("chapters")

    listed = chapters.search(Query().book_id == book_id)

    # trim data
    for item in listed:
        item["translated"] = ""
        item["original"] = ""

    return TypeAdapter(type=List[Chapter]).validate_python(listed)
