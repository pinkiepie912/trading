from fastapi import FastAPI

from .config import Config
from .database import db


def create_app(config: Config) -> FastAPI:
    # Create FastAPI app.
    app = FastAPI()

    # DB initializing
    db.init_app(app, config=config.TRADING_SQLALCHEMY_DATABASE)

    return app
