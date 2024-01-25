from datetime import datetime
from enum import Enum
from typing import ClassVar, Optional
from pydantic import BaseModel, constr

class Categories(str, Enum):
    FICTION = "fiction"
    FANTASY = "fantasy"
    DYSTOPIAN = "dystopian"
    ADVENTURE = "adventure"
    ROMANCE = "Romance"
    MYSTERY = "mystery"
    HORROR = "horror"
    THRILLER = "thriller"
    HISTORICAL = "historical"
    BIOGRAPHY = "biography"
    COOKING = "cooking"
    ART = "art"
    PHOTOGRAPHY = "photography"
    PERSONAL_DEVELOPMENT = "personal development"
    MOTIVATIONAL = "motivational"
    EDUCATION_ = "education"
    TRAVEL = "travel"
    SPIRITUALITY = "spirituality"
    
class BookCreate(BaseModel):
    title: constr(to_upper=True)
    page_count: int
    description: str
    status: Optional[bool] = True
    categories: Categories


class BookUpdate(BaseModel):
    IS_DELETED : ClassVar[str] = "is_deleted"
    
    title: constr(to_upper=True)
    page_count: int
    description: str
    status: Optional[bool] = True
    categories: str
    is_deleted: Optional[bool] = False

class BookResponse(BaseModel):
    id: int
    title: str
    description: str
    authors: str

class Book(BookResponse):
    categories: str
    published_date: datetime
    page_count: int

class BookOut(BaseModel):
    Books: Book
    likes: int
    reviews : int
feat-added-average-rating
    average_rating : Optional[float] = None

