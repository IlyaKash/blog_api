from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CommentBase(BaseModel):
    content: str=Field(... , min_length=1, max_length=1000)

class CommentCreate(CommentBase):
    article_id: int

class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    author_id: int
    article_id: int

    class Config:
        from_attributes=True

class CommnetUpdate(CommentBase):
    pass
