from typing import Generator, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

__all__ = ("FastAPISqlalchemy", "DBConfig")


class DBConfig(BaseModel):
    DB_URI: str
    POOL_RECYCLE: int = 900
    ECHO: bool = False


class FastAPISqlalchemy:
    def __init__(
        self,
        app: Optional[FastAPI] = None,
        *,
        config: Optional[DBConfig] = None,
    ):
        self._engine: Optional[Engine] = None
        self._session: Optional[sessionmaker] = None
        if app is not None and config is not None:
            self.init_app(app, config=config)

    def init_app(self, app: FastAPI, *, config: DBConfig):
        self._engine = create_engine(
            config.DB_URI,
            echo=config.ECHO,
            pool_recycle=config.POOL_RECYCLE,
        )

        self._session = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

        @app.on_event("startup")
        def setup():
            self._engine.connect()

        @app.on_event("shutdown")
        def teardown():
            self._session.close_all()
            self._engine.dispose()

    def get_session(self) -> Generator[Session, None, None]:
        if self._session is None:
            raise ValueError("Call get_session before init_app.")

        session = self._session()
        try:
            yield session
        finally:
            session.close()

    @property
    def engine(self) -> Engine:
        if self._engine is None:
            raise ValueError("Engine is not set yet. Call init_app first.")
        return self._engine
