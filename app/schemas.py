from datetime import datetime

from typing import ClassVar, Optional
from pydantic import BaseModel, EmailStr, conint


class MyBaseModel(BaseModel):
    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    page_count: int
    description: str
    status: Optional[bool] = True
    categories: str


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    IS_DELETED : ClassVar[str] = "is_deleted"
    
    title: str
    page_count: int
    description: str
    status: Optional[bool] = True
    categories: str
    is_deleted: Optional[bool] = False


class UsersData(MyBaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class BookResponse(BaseModel):
    title: str
    description: str
    authors: str
    isbn: int
    # description : str


class Book(BookResponse):
    categories: str
    published_date: datetime
    page_count: int


class BookOut(BaseModel):
    Books: Book
    likes: int


class UsersCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str


class UsersDelete(BaseModel):
    IS_DELETED: ClassVar[str] = "is_deleted"

    is_deleted: bool = True
    password: str


class LoginDetail(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    username: str


class Like(BaseModel):
    book_isbn: int
    dir: conint(ge=0, le=1)
