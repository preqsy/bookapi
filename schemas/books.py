from datetime import datetime
from typing import ClassVar, Optional
from pydantic import BaseModel, constr


class BookCreate(BaseModel):
    title: constr(to_upper=True)
    page_count: int
    description: str
    status: Optional[bool] = True
    categories: str


class BookUpdate(BaseModel):
    IS_DELETED : ClassVar[str] = "is_deleted"
    
    title: constr(to_upper=True)
    page_count: int
    description: str
    status: Optional[bool] = True
    categories: str
    is_deleted: Optional[bool] = False

class BookResponse(BaseModel):
    title: str
    description: str
    authors: str
    id: int

class Book(BookResponse):
    categories: str
    published_date: datetime
    page_count: int

class BookOut(BaseModel):
    Books: Book
    likes: int
    reviews : int