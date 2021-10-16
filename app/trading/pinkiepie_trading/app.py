from fastapi import FastAPI, status

from .config import Config
from .database import db
from .stock.controllers import stock_firm_router


def create_app(config: Config) -> FastAPI:
    # Create FastAPI app.
    app = FastAPI()

    # Health check
    @app.get("/health", status_code=status.HTTP_200_OK)
    async def health():
        return {"status": "ok"}

    # Add routers
    app.include_router(stock_firm_router)

    # DB initializing
    db.init_app(app, config=config.TRADING_SQLALCHEMY_DATABASE)

    return app
