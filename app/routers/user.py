from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from database import get_async_session
from schemas.user import UserCreate, UserResponse, UserInDB
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from auth import get_password_hash, get_current_user


router=APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/create_user", response_model=UserResponse)
async def add_user(user: UserCreate, session: AsyncSession= Depends(get_async_session)):
    result = await session.execute(select(User).where(User.username == user.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким username уже существует"
        )

    result =await session.execute(select(User).where(User.email==user.email))
    existing_user=result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )

    new_user=User(
        email=user.email, 
        username=user.username,
        hashed_password=get_password_hash(user.password),
        is_active=True,
        is_superuser=False,
        )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.delete("/delete_user", status_code=status.HTTP_200_OK)
async def delete_user(current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession=Depends(get_async_session)):
    result = await session.execute(select(User).where(User.username==current_user.username))
    existing_user = result.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с username '{current_user.username}' не найден"
        )
    
    await session.delete(existing_user)
    await session.commit()

    return {"detail": f"Пользователь '{current_user.username}' успешно удален"}
