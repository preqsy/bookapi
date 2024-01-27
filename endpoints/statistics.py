from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from app import models

from app.database import  get_db
from app.models import Books
from schemas.books import BookOut

router = APIRouter(prefix="/books/stats")

@router.get("/popular-books",response_model=List[BookOut])
def get_popular_books(db: Session = Depends(get_db)):
    most_liked_books = (
        db.query(
            models.Books,
            func.count(models.Like.book_id).label("likes")
            )
            .outerjoin(models.Like, models.Like.book_id == models.Books.id)
            .group_by(Books.id)
            .order_by(func.count(models.Like.book_id).desc())
            .all()
    )
    data = []
    for post in most_liked_books:
        data.append(post._asdict())
    return data