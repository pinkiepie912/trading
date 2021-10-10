from pydantic import BaseSettings

from .database.rdb import DBConfig


class Config(BaseSettings):
    TRADING_SQLALCHEMY_DATABASE: DBConfig
