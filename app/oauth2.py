import os
from datetime import datetime, timedelta

from dotenv import load_dotenv, find_dotenv
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import schemas
from app.database import get_db
from . import models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv(find_dotenv())
SECRET_KEY = os.environ.get("SECRET_KEY")
# EXPIRY_TIME = os.environ.get("EXPIRY_TIME")
ALGORITHM = os.environ.get("ALGORITHM")


EXPIRY_TIME = 30


def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRY_TIME)
    to_encode.update({"exp": expire})
    jwt_access_code = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return jwt_access_code

def verify_access_token(token, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id :str = payload.get("user_id")
        user_name : str = payload.get("user_name")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id, username=user_name)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could'nt validate credential", headers={"WWW-Authenticate":"Bearer"})
    token =  verify_access_token(token=token, credentials_exception=credentials_exception)
    user_details = db.query(models.Users).filter(models.Users.username == token.username).first()
    
    if user_details.is_deleted == True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account not found")
    return user_details
    