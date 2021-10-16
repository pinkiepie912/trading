import pytest
from trading_db.rdb.constants import Currency, StockType

from pinkiepie_trading.stock.repositories.ticker_reader import TickerReader


@pytest.mark.asyncio
async def test_get_list(session, firm_factory, ticker_factory):
    # given
    ticker_cnt = 10
    firm = await firm_factory(id=1, name="KB증권", trading_fee=0.1)
    for i in range(ticker_cnt):
        await ticker_factory(
            stock_type=StockType.STOCK,
            name="apple",
            ticker=f"test_ticker_{i}",
            firm=firm,
            fee=0.05,
            tax=0.05,
            currency=Currency.KRW,
        )

    reader = TickerReader(session)

    # when
    tickers = await reader.get_list()

    # then
    assert len(tickers) == ticker_cnt


@pytest.mark.asyncio
async def test_get_by(session, firm_factory, ticker_factory):
    # given
    target_ticker = "APPL"
    firm = await firm_factory(id=1, name="KB증권", trading_fee=0.1)
    await ticker_factory(
        stock_type=StockType.STOCK,
        name="apple",
        ticker=target_ticker,
        firm=firm,
        fee=0.05,
        tax=0.05,
        currency=Currency.KRW,
    )

    reader = TickerReader(session)

    # when
    ticker = await reader.get_by(target_ticker)

    # then
    assert ticker


@pytest.mark.asyncio
async def test_get_by_no_ticker(session):
    # given
    ticker = "NOTICKER"
    reader = TickerReader(session)

    # when
    ticker = await reader.get_by(ticker)

    # then
    assert not ticker
