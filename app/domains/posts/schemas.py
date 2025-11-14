# app/domains/posts/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostCreate(BaseModel):
    user_id: int
    caption: Optional[str] = None
    media_url: Optional[str] = None

class PostOut(BaseModel):
    id: int
    user_id: int
    caption: Optional[str]
    media_url: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
