import datetime

import pytest
from sqlalchemy.future import select
from trading_db.rdb.constants import Currency, StockType
from trading_db.rdb.stock.tickers import StockTicker as SAStockTicker
from trading_db.rdb.stock_firm.firm import Firm as SAStockFirm

from pinkiepie_trading.stock.models.stock_firm import StockFirm
from pinkiepie_trading.stock.repositories.stock_firm_reader import (
    StockFirmReader,
)
from pinkiepie_trading.stock.repositories.stock_firm_writer import (
    StockFirmWriter,
)
from pinkiepie_trading.stock.repositories.ticker_reader import TickerReader
from pinkiepie_trading.stock.repositories.ticker_writer import TickerWriter
from pinkiepie_trading.stock.services.stock_reader import StockReader
from pinkiepie_trading.stock.services.stock_registerer import StockRegisterer


@pytest.mark.asyncio
async def test_register_firm(request, session):
    # given
    name = "KB증권"
    trading_fee = 0.1

    registerer = StockRegisterer(
        stock_firm_writer=StockFirmWriter(session),
        ticker_writer=TickerWriter(session),
        stock_reader=StockReader(
            stock_firm_reader=StockFirmReader(session),
            ticker_reader=TickerReader(session),
        ),
    )

    # when
    await registerer.register_firm(name=name, trading_fee=trading_fee)

    # then
    query = await session.execute(select(SAStockFirm).filter_by(name=name))
    sa_stock_firm = query.scalar()

    assert sa_stock_firm


@pytest.mark.asyncio
async def test_register_ticker(request, session, firm_factory):
    # given
    now = datetime.datetime.now(tz=datetime.timezone.utc)

    name = "apple"
    ticker = "APPL"
    currency = Currency.KRW
    stock_type = StockType.STOCK
    fee = 0.05
    tax = 0.05
    stock_firm = StockFirm.of(
        await firm_factory(name="KB증권", trading_fee=0.1, created_at=now)
    )

    registerer = StockRegisterer(
        stock_firm_writer=StockFirmWriter(session),
        ticker_writer=TickerWriter(session),
        stock_reader=StockReader(
            stock_firm_reader=StockFirmReader(session),
            ticker_reader=TickerReader(session),
        ),
    )

    # when
    await registerer.register_ticker(
        name=name,
        ticker=ticker,
        currency=currency.value,
        stock_type=stock_type.value,
        fee=fee,
        tax=tax,
        firm_id=stock_firm.id,
    )

    # then
    query = await session.execute(select(SAStockTicker).filter_by(name=name))
    sa_stock_ticker = query.scalar()

    assert sa_stock_ticker
