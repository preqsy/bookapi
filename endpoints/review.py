from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from app.oauth2 import get_current_user

from app.schemas import ReviewCreate

router = APIRouter(prefix="/books/{id}/reviews", tags=["Reviews"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_review(id: str, review:ReviewCreate, db:Session = Depends(get_db), current_user: int =Depends(get_current_user)):
    new_review = models.Reviews(user_id=current_user.id, review=review.review, book_id=id)
    db.add(new_review)
    db.commit()
    return review.review

@router.get("/", status_code=status.HTTP_200_OK)
def get_reviews(id: str, db:Session = Depends(get_db)):
    reviews = db.query(models.Reviews).filter(models.Reviews.book_id == id).all()
    if reviews == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No reviews found")
    return reviews
