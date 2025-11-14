from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    display_name: Optional[str]
    bio: Optional[str]

class UserOut(BaseModel):
    id: int
    username: str
    display_name: Optional[str]
    bio: Optional[str]
    created_at: datetime
    class Config:
        orm_mode = True


# checka 
class UserLogin(BaseModel):
    username: str
    password: str

