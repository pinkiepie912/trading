from pydantic import BaseSettings

from .database.db import DBConfig


class Config(BaseSettings):
    TRADING_SQLALCHEMY_DATABASE: DBConfig
