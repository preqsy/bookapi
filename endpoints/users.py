from fastapi import APIRouter, HTTPException,status, Depends
from app.oauth2 import get_current_user
from app.schemas import *
from sqlalchemy.orm import Session
from app.database import *
from app import models
from app.utils import hash, verify
from typing import List

router = APIRouter(
    prefix="/users"
)
@router.get("/", response_model=List[UsersData], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    if users == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UsersData)
def create_user(user: UsersCreate, db : Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete(user : UsersDelete, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    user_query = db.query(models.Users).filter(current_user.id == models.Users.id)
    if not user_query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
    if not verify(new_password=user.password, hashed_password=user_query.first().password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Password is needed before account deletion")
    user_query.update({"is_deleted" : user.is_deleted})
    db.commit()
    return "Account Deleted"
    
    