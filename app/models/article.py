from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Article(Base):
    __tablename__="articles"
    
    id=Column(Integer, primary_key=True)
    title=Column(String(100), nullable=False)
    content=Column(String(10000), nullable=False)
    author_id=Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article")