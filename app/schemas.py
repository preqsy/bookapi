from datetime import datetime
from enum import Enum

from typing import ClassVar, Optional
from pydantic import BaseModel, EmailStr, conint, constr, root_validator


class MyBaseModel(BaseModel):
    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: constr(to_upper=True)
    page_count: int
    description: str
    status: Optional[bool] = True
    categories: str


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    IS_DELETED : ClassVar[str] = "is_deleted"
    
    title: constr(to_upper=True)
    page_count: int
    description: str
    status: Optional[bool] = True
    categories: str
    is_deleted: Optional[bool] = False


class UsersData(MyBaseModel):
    first_name: str
    last_name: str
    username : str
    email: EmailStr


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


class UsersCreate(BaseModel):
    first_name: str
    last_name: str
    username: constr(to_lower=True)
    email: EmailStr
    password: str
    
class ReasonsEnum(str, Enum):
    FOUND_ALTERNATIVE = "found an alternative"
    NOT_ENOUGH_FEATURES = "missing features"
    PRIVACY_ISSUES = "privacy concerns"
    HARD_TO_USE = "difficult to use"
    NOT_ENOUGH_OPTIONS = "limited options"
    SECURITY_CONCERNS = "security worries"
    TESTING_OTHER_SERVICES = "trying other services"


class UsersDelete(BaseModel):
    IS_DELETED: ClassVar[str] = "is_deleted"
    REASON: ClassVar[str] = "reason_for_deletion"

    is_deleted: bool = True
    reason_for_deletion: ReasonsEnum
    password: str
    
    @root_validator(pre=True)
    def check_reason(cls, values):
        reason = values.get(cls.REASON)
        if not reason:
            raise ValueError("Reason for deletion is required")
        return values


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
    dir: conint(ge=0, le=1)
    
class ReviewCreate(BaseModel):
    review: str
    rating: conint(strict=True, ge=1, le=5) 
    
class ReviewResponse(BaseModel):
    user_id: int
    review: str
    rating: int
    owner : UsersData
