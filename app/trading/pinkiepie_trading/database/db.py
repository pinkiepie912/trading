from typing import AsyncGenerator, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

__all__ = ("FastAPISqlalchemy", "DBConfig")


class DBConfig(BaseModel):
    URI: str
    DB_NAME: str
    POOL_RECYCLE: int = 900
    ECHO: bool = False

    @property
    def db_uri(self) -> str:
        return f"{self.URI}/{self.DB_NAME}"


class FastAPISqlalchemy:
    def __init__(
        self,
        app: Optional[FastAPI] = None,
        *,
        config: Optional[DBConfig] = None,
    ):
        self._engine: Optional[AsyncEngine] = None
        self._session: Optional[sessionmaker] = None
        if app is not None and config is not None:
            self.init_app(app, config=config)

    def init_app(self, app: FastAPI, *, config: DBConfig):
        self._engine = create_async_engine(
            config.db_uri,
            echo=config.ECHO,
            pool_recycle=config.POOL_RECYCLE,
        )

        self._session = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

        @app.on_event("shutdown")
        async def teardown():
            self._session.close_all()
            await self._engine.dispose()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        if self._session is None:
            raise ValueError("Call get_session before init_app.")

        async with self._session() as session:
            yield session

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            raise ValueError("Engine is not set yet. Call init_app first.")
        return self._engine
