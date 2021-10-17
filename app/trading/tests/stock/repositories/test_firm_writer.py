import datetime

import pytest
from sqlalchemy import select
from trading_db.rdb.constants import Currency, StockType
from trading_db.rdb.stock.tickers import StockTicker as SAStockTicker
from trading_db.rdb.stock_firm.firm import Firm as SAStockFirm

from pinkiepie_trading.stock.models.stock_firm import StockFirm
from pinkiepie_trading.stock.repositories.stock_firm_writer import (
    StockFirmWriter,
)


@pytest.mark.asyncio
async def test_save(session):
    # given
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    stock_firm = StockFirm(
        id=None, name="KB증권", trading_fee=0.1, created_at=now
    )

    writer = StockFirmWriter(session)

    # when
    await writer.save(stock_firm)

    # then
    query = select(SAStockFirm).where(SAStockFirm.name == stock_firm.name)
    sa_stock_firm = (await session.execute(query)).scalar()

    assert sa_stock_firm


@pytest.mark.asyncio
async def test_soft_deletion(session, firm_factory, ticker_factory):
    # given
    sa_firm = await firm_factory(name="KB증권", trading_fee=0.1)

    # Tickers
    for i in range(2):
        await ticker_factory(
            stock_type=StockType.STOCK,
            name="apple",
            ticker=f"test_ticker_{i}",
            firm=sa_firm,
            fee=0.05,
            tax=0.05,
            currency=Currency.KRW,
        )
    writer = StockFirmWriter(session)

    # when
    await writer.delete(sa_firm.id, soft=True)

    # then
    assert sa_firm.deleted_at is not None
    for ticker in sa_firm.tickers:
        assert ticker.deleted_at is not None


@pytest.mark.asyncio
async def test_hard_deletion(session, firm_factory, ticker_factory):
    # given
    sa_firm = await firm_factory(name="KB증권", trading_fee=0.1)
    sa_tickers = [
        await ticker_factory(
            stock_type=StockType.STOCK,
            name="apple",
            ticker=f"test_ticker_{i}",
            firm=sa_firm,
            fee=0.05,
            tax=0.05,
            currency=Currency.KRW,
        )
        for i in range(2)
    ]
    writer = StockFirmWriter(session)

    # when
    await writer.delete(sa_firm.id, soft=False)

    # then
    query = select(SAStockFirm).where(SAStockFirm.id == sa_firm.id)
    sa_firm = (await session.execute(query)).scalar()
    assert sa_firm is None

    query = select(SAStockTicker).where(
        SAStockTicker.id.in_([ticker.id for ticker in sa_tickers])
    )
    sa_tickers = (await session.execute(query)).scalars().all()
    assert len(sa_tickers) == 0
