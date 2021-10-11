from pydantic import BaseSettings

from .database.rdb import DBConfig


class Config(BaseSettings):
    ENV: str
    TRADING_SQLALCHEMY_DATABASE: DBConfig
