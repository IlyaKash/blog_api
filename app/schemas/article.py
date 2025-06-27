from pydantic import BaseModel
from typing import Optional


class ArticleCreate(BaseModel):
    title:str
    content:str

    
class ArticleResponse(ArticleCreate):
    id: int
    author_id: int

class ArticleUpdate(BaseModel):
    title: str
    content: str

class ArticlePatch(BaseModel):
    title: Optional[str]=None
    content: Optional[str]=None

