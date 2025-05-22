from pydantic import BaseModel

class ArticleCreate(BaseModel):
    title:str
    content:str

class ArticleResponse(ArticleCreate):
    id: int
    author_id: int