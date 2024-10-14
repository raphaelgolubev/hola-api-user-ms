from enum import Enum
from pydantic import BaseModel, EmailStr


class UserType(str, Enum):
    business = "Business"
    customer = "Customer"
    moderator = "Moderator"


class UserSchema(BaseModel):
    email: EmailStr
    phone: str
    password: str
    user_type: UserType
    is_email_verified: bool | None = None
    is_blocked: bool | None = None