from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str=Field(... , min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str =Field(... , min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr]=None
    username: Optional[str]=Field(None, min_length=3, max_length=50)
    password: Optional[str]=Field(None, min_length=8)

class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    

    class Config:
        from_attributes=True

class UserResponse(UserBase):
    is_active: bool

class UserPublic(UserInDB):
    articles_count: int
    comments_count: int