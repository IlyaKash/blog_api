from fastapi import APIRouter, Depends, HTTPException, status
from schemas.article import ArticleCreate, ArticleResponse, ArticleUpdate, ArticlePatch
from models.article import Article
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from database import get_async_session
from auth import get_current_user
from schemas.user import UserInDB

router=APIRouter(
    prefix="/article",
    tags=["article"]
)

@router.post("/create_article", response_model=ArticleResponse)
async def new_article(
        article: Annotated[ArticleCreate, Depends()],
        session: AsyncSession=Depends(get_async_session),
        user: UserInDB=Depends(get_current_user)
):
    new_article=Article(
        title=article.title,
        content=article.content,
        author_id=user.id
    )
    session.add(new_article)
    await session.commit()
    await session.refresh(new_article)
    return new_article

@router.get("/my_articles", response_model=List[ArticleResponse])
async def all_my_articles(
    current_user: UserInDB=Depends(get_current_user),
    session: AsyncSession=Depends(get_async_session)
):
    result=await session.execute(select(Article).where(Article.author_id==current_user.id))
    articles=result.scalars().all()
    return articles

@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article_by_id(
    article_id: int,
    current_user: UserInDB=Depends(get_current_user),
    session: AsyncSession=Depends(get_async_session)
):
    result = await session.execute(select(Article).where(Article.id==article_id))
    existing_article=result.scalar()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"This article by user {current_user.username} with id={article_id} does not exist"
        )
    return  existing_article


@router.put("/{article_id}", response_model=ArticleResponse)
async def full_update_article(
    article_id: int,
    update_data: Annotated[ArticleUpdate, Depends()],
    current_user: UserInDB=Depends(get_current_user),
    session: AsyncSession=Depends(get_async_session),   
):
    stmt=(
        update(Article)
        .where(Article.id==article_id)
        .values(**update_data.model_dump(exclude_unset=True))
        .execution_options(synchronize_session="fetch")
    )
    await session.add(stmt)
    await session.commit()

    result = await session.execute(select(Article).where(Article.id==article_id))
    update_article=result.scalar_one()

    return update_article


@router.patch("/{article_id}", response_model=ArticleResponse)
async def partial_update_article(
    article_id: int,
    update_data: Annotated[ArticlePatch, Depends()],
    current_user: UserInDB=Depends(get_current_user),
    session: AsyncSession=Depends(get_async_session)
):
    stmt=(
        update(Article)
        .where(Article.id==article_id)
        .values(**update_data.model_dump(exclude_unset=True, exclude_none=True))
    )
    await session.add(stmt)
    await session.commit()

    result = await session.execute(select(Article).where(Article.id==article_id))
    update_article=result.scalar_one()
    
    return update_article


@router.delete("/{article_id}")
async def delete_article(
    article_id: int,
    current_user: UserInDB=Depends(get_current_user),
    session: AsyncSession=Depends(get_async_session)
):
    result=await session.execute(select(Article).where(Article.id==article_id))
    existing_article=result.scalar()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"This article by user {current_user.username} with id={article_id} does not exist"
        )
    await session.delete(existing_article)
    await session.commit()

    return {"detail": f"The article with id={article_id} successfully deleted"}