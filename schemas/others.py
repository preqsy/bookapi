from typing import Optional
from pydantic import BaseModel, EmailStr, conint


class LoginDetail(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    username: str


class Like(BaseModel):
    dir: conint(ge=0, le=1)