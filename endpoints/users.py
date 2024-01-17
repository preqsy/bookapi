from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.oauth2 import get_current_user
from app.schemas import UsersCreate, UsersData, UsersDelete
from app.database import get_db
from app import models
from app.utils import hash, verify


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UsersData], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    if users == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
        )
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UsersData)
def create_user(user: UsersCreate, db: Session = Depends(get_db)):
    if not user.password or not user.email or not user.username or not user.first_name or not user.last_name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Input all fields")
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    return new_user


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete(
    user: UsersDelete,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user_query = db.query(models.Users).filter(current_user.id == models.Users.id)
    
    if not user_query:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not found"
        )
    if not user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Password is needed before deleting account"
        )
    if not verify(
        new_password=user.password, hashed_password=user_query.first().password
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Password not correct",
        )
    user_query.update({user.IS_DELETED: user.is_deleted, user.REASON: user.reason_for_deletion})
    user_posts_query = db.query(models.Books).filter(
        models.Books.authors == current_user.username
    )
    user_posts_query.update({user.IS_DELETED : user.is_deleted})
    db.commit()
    return "Account Deleted"
