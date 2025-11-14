
# include all models 

from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.core.db import Base


class Follow(Base):
    __tablename__ = "follows"
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    followee_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())



# class Comment(Base):
#     __tablename__ = "comments"
#     id = Column(Integer, primary_key=True)
#     post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
#     text = Column(Text)
#     created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

#     post = relationship("Post", back_populates="comments")

# class Like(Base):
#     __tablename__ = "likes"
#     id = Column(Integer, primary_key=True)
#     post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
#     created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

#     post = relationship("Post", back_populates="likes")
