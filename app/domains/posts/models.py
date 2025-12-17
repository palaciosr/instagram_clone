
# include all models 

from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func, LargeBinary
from sqlalchemy.orm import relationship
from app.core.db import Base

from datetime import datetime

class Post(Base):
    __tablename__ = "posts"

    # need to add contents and url can be none

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    caption = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")

    # optional
    file_name = Column(String, nullable=True)
    image_data = Column(LargeBinary, nullable=True) # content


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String)
    user = relationship("User")
    post = relationship("Post", back_populates="comments")


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    post = relationship("Post", back_populates="likes")
    user = relationship("User")

