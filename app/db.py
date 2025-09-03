# Ref: https://github.com/fastapi-users/fastapi-users/blob/v14.0.1/examples/sqlalchemy/app/db.py
from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import User

DATABASE_URL = "sqlite+aiosqlite:///./test.db"


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,  # Use SQLModel's AsyncSession
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase]:
    yield SQLAlchemyUserDatabase(session, User)
