from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Comment(Base):
    __tablename__="comments"

    id=Column(Integer, primary_key=True)
    content=Column(String(1000), nullable=False)
    created_at=Column(DateTime(timezone=True), server_default=func.now())

    author_id=Column(Integer, ForeignKey("users.id"))

    article_id=Column(Integer, ForeignKey("articles.id"))
    author = relationship("User", back_populates="comments")
    article = relationship("Article", back_populates="comments")