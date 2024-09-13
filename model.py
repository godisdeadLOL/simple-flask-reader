from typing import Optional
from pydantic import BaseModel


class Chapter(BaseModel):
    book_id: str
    number: int
    title: str
    translated: str
    original: Optional[str]

class Book(BaseModel):
    book_id: str
    title: str