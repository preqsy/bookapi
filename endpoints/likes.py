from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(prefix="/books/{id}/like", tags=["Likes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(
    id: str,
    like: schemas.Like,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    book_query = (
        db.query(models.Books).filter(models.Books.id == id).first()
    )
    if not book_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {id} doesn't exist",
        )

    like_query = db.query(models.Like).filter(
        models.Like.book_id == id, models.Like.user_id == current_user.id
    )
    liked = like_query.first()

    if like.dir == 1:
        if liked:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Book already liked by you",
            )
        new_like = models.Like(book_id=id, user_id=current_user.id)
        db.add(new_like)
        response = "Liked"
    else:
        if not liked:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't exist"
            )
        like_query.delete()
        response = "Unliked"

    db.commit()
    return {"detail": response}
