from fastapi import APIRouter, Depends, HTTPException, status
from schemas.comment import CommentCreate, CommentResponse, CommnetUpdate
from models.comment import Comment
from typing import List, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from database import get_async_session
from auth import get_current_user
from schemas.user import UserInDB
from schemas.article import ArticleResponse

router=APIRouter(
    prefix="/comment",
    tags=["comment"]
)


@router.post("/create_comment", response_model=CommentResponse)
async def add_comment(
    comment: Annotated[CommentCreate, Depends()],
    article_id: int,
    session: AsyncSession=Depends(get_async_session),
    user: UserInDB=Depends(get_current_user)
):
    new_comment=Comment(
        article_id=article_id,
        content=comment.content,
        author_id=user.id
    )
    session.add(new_comment)
    await session.commit()
    await session.refresh(new_comment)
    return new_comment


@router.get("/get_all_comments_by_id_post", response_model=List[CommentResponse])
async def get_comments_on_the_article(
    article_id: int,
    session: AsyncSession=Depends(get_async_session),
    user: UserInDB=Depends(get_current_user)
):
    result=await session.execute(select(Comment).where(Comment.article_id==article_id))
    comments=result.scalars().all()
    return comments

@router.get("/get_all_comments_by_id_user", response_model=List[CommentResponse])
async def get_comments_on_the_user(
    another_user_id: int,
    session: AsyncSession=Depends(get_async_session),
    user: UserInDB=Depends(get_current_user)
):
    result=await session.execute(select(Comment).where(Comment.author_id==another_user_id))
    comments=result.scalars().all()
    return comments


@router.put("/{comment_id}", response_model=CommentResponse)
async def full_update_comment(
    comment_id: int,
    update_data: Annotated[CommnetUpdate, Depends()],
    session: AsyncSession=Depends(get_async_session),
    user: UserInDB=Depends(get_current_user)
):
    pass
    