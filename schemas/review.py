from pydantic import BaseModel, conint

from .users import UsersData


class ReviewCreate(BaseModel):
    review: str
    rating: conint(strict=True, ge=1, le=5) 
    
class ReviewResponse(BaseModel):
    user_id: int
    review: str
    rating: int
    owner : UsersData