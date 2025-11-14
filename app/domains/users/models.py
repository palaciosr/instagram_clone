


from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func, LargeBinary
from sqlalchemy.orm import relationship
from app.core.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    display_name = Column(String(128))
    bio = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    posts = relationship("Post", back_populates="user")

