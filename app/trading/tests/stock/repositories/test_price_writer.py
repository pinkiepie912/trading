import datetime

import pytest
from sqlalchemy.future import select
from trading_db.rdb.constants import Currency, StockType
from trading_db.rdb.stock.price import Price as SAPrice

from pinkiepie_trading.stock.models.price import Price, PriceHistory
from pinkiepie_trading.stock.repositories.price_writer import PriceWriter


@pytest.mark.asyncio
async def test_save(session, firm_factory, ticker_factory):
    # given
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    firm = await firm_factory(name="KB증권", trading_fee=0.1)
    ticker = await ticker_factory(
        stock_type=StockType.STOCK,
        name="apple",
        ticker="APPL",
        firm=firm,
        fee=0.05,
        tax=0.05,
        currency=Currency.KRW,
    )
    session.add(firm)
    session.add(ticker)
    await session.commit()

    price = Price(
        id=None,
        adj_close=100.1,
        close=100.1,
        high=110.1,
        low=90.1,
        open=95.1,
        volume=100000,
        date_time=now,
        ticker_id=ticker.id,
        currency=Currency.USD,
    )

    writer = PriceWriter(session)

    # when
    await writer.save(price)

    # then
    query = select(SAPrice).where(SAPrice.ticker == ticker)
    sa_price = (await session.execute(query)).scalar()

    assert sa_price


@pytest.mark.asyncio
async def test_save_history(session, firm_factory, ticker_factory):
    # given
    now = datetime.datetime.now(tz=datetime.timezone.utc)

    firm = await firm_factory(name="KB증권", trading_fee=0.1)
    ticker = await ticker_factory(
        stock_type=StockType.STOCK,
        name="apple",
        ticker="APPL",
        firm=firm,
        fee=0.05,
        tax=0.05,
        currency=Currency.KRW,
    )

    history_length = 10
    history = PriceHistory(
        currency=Currency.USD,
        prices=[
            Price(
                id=None,
                adj_close=100.1,
                close=100.1,
                high=110.1,
                low=90.1,
                open=95.1,
                volume=100000,
                date_time=now + datetime.timedelta(hours=i),
                ticker_id=ticker.id,
                currency=Currency.USD,
            )
            for i in range(history_length)
        ],
    )

    writer = PriceWriter(session)

    # when
    await writer.save_history(history)

    # then
    query = select(SAPrice).where(SAPrice.ticker == ticker)
    prices = (await session.execute(query)).scalars().all()

    assert len(prices) == history_length
