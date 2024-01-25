from fastapi import APIRouter, Depends
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from app import models

from app.database import  get_db
from app.models import Books

router = APIRouter(prefix="/books")

@router.get("/popular-books")
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
    return most_liked_books