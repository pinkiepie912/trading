import logging
import os

import pytest
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import create_database, drop_database
from trading_db.rdb.base import Model
from trading_db.rdb.coin.bitcoin import Bitcoin
from trading_db.rdb.stock.price import Price
from trading_db.rdb.stock.tickers import StockTicker
from trading_db.rdb.stock_firm.firm import Firm

logger = logging.getLogger(__name__)


try:
    load_dotenv(find_dotenv("../.env-test"))
except IOError:
    pass


@pytest.fixture(scope="session")
def engine():
    uri = os.environ["TRADING_SQLALCHEMY_DATABASE_URI"]
    engine = create_engine(uri, echo=True)
    yield engine


@pytest.fixture(scope="session")
def database_schema(engine):
    try:
        create_database(engine.url)
    except Exception as e:
        logger.warning("Exception raised while creating database", exc_info=e)

    Model.metadata.create_all(engine)

    try:
        yield
    finally:
        drop_database(engine.url)


@pytest.fixture(scope="function")
def session(engine, database_schema):
    factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    _session = scoped_session(factory)

    _session.begin_nested()
    yield _session
    _session.rollback()


@pytest.fixture(scope="function")
def bitcoin_factory(session):
    def factory(*args, **kwargs):
        obj = Bitcoin(*args, **kwargs)
        session.add(obj)
        session.flush()

        return obj

    return factory


@pytest.fixture(scope="function")
def firm_factory(session):
    def factory(*args, **kwargs):
        obj = Firm(*args, **kwargs)
        session.add(obj)
        session.flush()

        return obj

    return factory


@pytest.fixture(scope="function")
def ticker_factory(session):
    def factory(*args, **kwargs):
        obj = StockTicker(*args, **kwargs)
        session.add(obj)
        session.flush()

        return obj

    return factory


@pytest.fixture(scope="function")
def price_factory(session):
    def factory(*args, **kwargs):
        obj = Price(*args, **kwargs)
        session.add(obj)
        session.flush()

        return obj

    return factory
