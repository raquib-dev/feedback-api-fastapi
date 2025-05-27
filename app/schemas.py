from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ---------------------------
# User schemas
# ---------------------------
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True

# ---------------------------
# Token schemas
# ---------------------------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

# ---------------------------
# Feedback schemas
# ---------------------------
class FeedbackBase(BaseModel):
    content: str = Field(..., min_length=1)

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackOut(FeedbackBase):
    id: int
    is_approved: bool
    is_deleted: bool
    created_at: datetime
    user_id: Optional[int]

    class Config:
        orm_mode = True
