from fastapi import FastAPI

from .config import Config
from .database import db
from .stock.controllers import stock_firm_router


def create_app(config: Config) -> FastAPI:
    # Create FastAPI app.
    app = FastAPI()

    # Add routers
    app.include_router(stock_firm_router)

    # DB initializing
    db.init_app(app, config=config.TRADING_SQLALCHEMY_DATABASE)

    return app
