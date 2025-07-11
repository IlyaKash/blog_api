from sqlalchemy import Integer,String, Column, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True)
    username=Column(String(50), unique=True, nullable=False)
    email=Column(String(255), unique=True, index=True, nullable=False)
    hashed_password=Column(String(255), nullable=False)
    is_active=Column(Boolean, default=True)
    is_superuser=Column(Boolean, default=False)
    created_at=Column(DateTime(timezone=True), server_default=func.now())

    comments = relationship("Comment", back_populates="author")
    articles = relationship("Article", back_populates="author")

