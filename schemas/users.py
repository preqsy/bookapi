from enum import Enum
from typing import ClassVar
from pydantic import BaseModel, EmailStr, constr, root_validator


class UsersCreate(BaseModel):
    first_name: str
    last_name: str
    username: constr(to_lower=True)
    email: EmailStr
    password: str
    

class UsersData(BaseModel):
    first_name: str
    last_name: str
    username : str
    email: EmailStr
    
class ReasonsEnum(str, Enum):
    FOUND_ALTERNATIVE = "found an alternative"
    NOT_ENOUGH_FEATURES = "missing features"
    PRIVACY_ISSUES = "privacy concerns"
    HARD_TO_USE = "difficult to use"
    NOT_ENOUGH_OPTIONS = "limited options"
    SECURITY_CONCERNS = "security worries"
    TESTING_OTHER_SERVICES = "trying other services"


class UsersDelete(BaseModel):
    IS_DELETED: ClassVar[str] = "is_deleted"
    REASON: ClassVar[str] = "reason_for_deletion"

    is_deleted: bool = True
    reason_for_deletion: ReasonsEnum
    password: str
    
    @root_validator(pre=True)
    def check_reason(cls, values):
        reason = values.get(cls.REASON)
        if not reason:
            raise ValueError("Reason for deletion is required")
        return values