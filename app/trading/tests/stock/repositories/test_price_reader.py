import datetime

import pytest
from trading_db.rdb.constants import Currency, StockType

from pinkiepie_trading.stock.repositories.price_reader import PriceReader


@pytest.mark.asyncio
async def test_get_history_by(
    session, firm_factory, ticker_factory, price_factory
):
    # given
    history_length = 10
    target_ticker = "AAPL"

    now = datetime.datetime.now(tz=datetime.timezone.utc)
    expected_length = 5
    start_date = now - datetime.timedelta(days=expected_length - 1)
    end_date = now

    firm = await firm_factory(id=1, name="KB증권", trading_fee=0.1)
    ticker = await ticker_factory(
        id=1,
        stock_type=StockType.STOCK,
        name="apple",
        ticker=target_ticker,
        firm=firm,
        fee=0.05,
        tax=0.05,
        currency=Currency.KRW,
    )

    for i in range(history_length):
        await price_factory(
            ticker=ticker,
            adj_close=100.1,
            close=100.1,
            high=110.1,
            low=90.1,
            open=95.1,
            volume=100000,
            date_time=now - datetime.timedelta(days=i),
            currency=Currency.KRW,
        )

    reader = PriceReader(session)

    # when
    history = await reader.get_history(ticker, start_date, end_date)

    # then
    assert history.currency == Currency.KRW
    assert len(history.prices) == expected_length
