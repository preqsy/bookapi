from app.database import get_db
from app import models
from app.schemas import LoginDetail
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.utils import verify
from app.oauth2 import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)
@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def auth_user(user: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user_details = db.query(models.Users).filter(models.Users.email == user.username).first()
    if not user_details:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid username")
    
    if not verify(new_password=user.password, hashed_password=user_details.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password")
    access_token = create_access_token({"user_id" : user_details.id, "user_name": user_details.username})
    return {"access_token" : access_token, "token_type" : "bearer"}
