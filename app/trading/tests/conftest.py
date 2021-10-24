import asyncio
import logging

import pytest
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, drop_database
from trading_db.rdb.asset.stock import StockAsset
from trading_db.rdb.base import Model
from trading_db.rdb.coin.bitcoin import Bitcoin
from trading_db.rdb.stock.price import Price
from trading_db.rdb.stock.tickers import StockTicker
from trading_db.rdb.stock_firm.firm import Firm

from pinkiepie_trading.app import create_app
from pinkiepie_trading.config import Config
from pinkiepie_trading.database import db
from pinkiepie_trading.utils.async_helper import anext

logger = logging.getLogger(__name__)


try:
    load_dotenv(find_dotenv(".env.test"), override=True)
except IOError:
    pass


@pytest.fixture(scope="session")
def app_config():
    # Load config from env
    config = Config()

    return config


@pytest.fixture(scope="session")
def app(app_config):

    # Create app
    app = create_app(app_config)

    return app


@pytest.fixture(scope="session")
def database_schema(app_config):
    db_config = app_config.TRADING_SQLALCHEMY_DATABASE

    # create_database and drop_database don't support async.
    uri = db_config.db_uri.replace("asyncpg", "psycopg2")
    engine = create_engine(uri)
    try:
        create_database(engine.url)
    except Exception as e:
        logger.warning("Exception raised while creating database", exc_info=e)

    Model.metadata.create_all(engine)

    try:
        yield
    finally:
        drop_database(engine.url)
        engine.dispose()


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="function")
async def session(app, database_schema):
    _session_generator = db.get_session()
    _session = await anext(_session_generator)

    # AsyncSession.commit to AsyncSession.flush for fast testing.
    _session.commit = _session.flush
    yield _session


@pytest.fixture(scope="function")
async def sync_session(session):
    yield session.sync_session


@pytest.fixture(scope="function")
def bitcoin_factory(session):
    async def factory(*args, **kwargs):
        obj = Bitcoin(*args, **kwargs)
        session.add(obj)
        await session.flush()

        return obj

    yield factory


@pytest.fixture(scope="function")
def firm_factory(session):
    async def factory(*args, **kwargs):
        obj = Firm(*args, **kwargs)
        session.add(obj)
        await session.flush()

        return obj

    yield factory


@pytest.fixture(scope="function")
def ticker_factory(session):
    async def factory(*args, **kwargs):
        obj = StockTicker(*args, **kwargs)
        session.add(obj)
        await session.flush()

        return obj

    yield factory


@pytest.fixture(scope="function")
def price_factory(session):
    async def factory(*args, **kwargs):
        obj = Price(*args, **kwargs)
        session.add(obj)
        await session.flush()

        return obj

    yield factory


@pytest.fixture(scope="function")
def stock_asset_factory(session):
    async def factory(*args, **kwargs):
        obj = StockAsset(*args, **kwargs)
        session.add(obj)
        await session.flush()

        return obj

    yield factory
