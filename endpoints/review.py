from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app import models
from app.database import get_db
from app.oauth2 import get_current_user

from app.schemas import ReviewCreate, ReviewResponse

router = APIRouter(prefix="/books/{id}/reviews", tags=["Reviews"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReviewCreate)
def add_review(
    id: str,
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    new_review = models.Reviews(
        user_id=current_user.id, review=review.review, book_id=id, rating=review.rating
    )
    db.add(new_review)
    db.commit()
    return review


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ReviewResponse])
def get_reviews(id: str, db: Session = Depends(get_db)):
    book_query = db.query(models.Books).filter(models.Books.id == id).first()
    if book_query.is_deleted == True:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    reviews = (
        db.query(models.Reviews)
        .filter(models.Reviews.book_id == id)
        .options(joinedload(models.Reviews.book))
        .all()
    )
    if reviews == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No reviews found"
        )
    return reviews
