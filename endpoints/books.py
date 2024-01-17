from typing import List, Optional

from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func


import app.models as models
from app.oauth2 import get_current_user
from app.database import get_db
from app.schemas import BookCreate, BookUpdate, BookResponse, BookOut
from app.utils import generate_isbn

router = APIRouter(prefix="/books")


@router.get("/", response_model=List[BookOut])
def get_all_books(
    db: Session = Depends(get_db),
    limit: Optional[int] = 10,
    search: Optional[str] = "",
):
    result = (
        db.query(
            models.Books,
            func.count(models.Like.book_id).label("likes"),
            func.count(models.Reviews.book_id).label("reviews"),
        )
        .outerjoin(models.Like, models.Like.book_id == models.Books.id)
        .outerjoin(models.Reviews, models.Reviews.book_id == models.Books.id)
        .group_by(models.Books.id)
        .filter(
            models.Books.title.contains(search.upper()) | models.Books.authors.contains(search.lower())
        )
        .filter(models.Books.is_deleted == False)
        .limit(limit)
        .all()
    )

    data = []
    for post in result:
        data.append(post._asdict())
    return data


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    new_post = models.Books(
        authors=current_user.username, isbn=generate_isbn(), **book.dict()
    )
    if not new_post:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Input all fields"
        )
    db.add(new_post)
    db.commit()
    return new_post


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=BookOut)
def single_book(
    id: int,
    db: Session = Depends(get_db),
):

    book = (
        db.query(
            models.Books,
            func.count(models.Like.book_id).label("likes"),
            func.count(models.Reviews.book_id).label("reviews"),
        )
        .outerjoin(models.Like, models.Like.book_id == models.Books.id)
        .outerjoin(models.Reviews, models.Reviews.book_id == models.Books.id)
        .group_by(models.Books.id)
        .filter(models.Books.id == id)
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ISBN: {id} does not exist",
        )
    return book


@router.delete("/{id}", response_model=List[BookResponse])
def delete_book(
    id: int,
    db: Session = Depends((get_db)),
    current_user: int = Depends(get_current_user),
):
    book_query = db.query(models.Books).filter(models.Books.id == id)
    book = book_query.first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with isbn: {id} does not exist",
        )

    if book.authors != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can't delete another user post",
        )
    book_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}", response_model=BookResponse, status_code=status.HTTP_202_ACCEPTED
)
def update_book(
    book: BookUpdate,
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    book_query = db.query(models.Books).filter(models.Books.id == id)
    updated_book = book_query.first()
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with isbn: {id} does not exist",
        )
    if updated_book.authors != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="can't updated another user's post",
        )

    book_query.update(book.dict(), synchronize_session=False)
    db.commit()

    return book_query.first()

