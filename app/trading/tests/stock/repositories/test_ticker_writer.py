import datetime

import pytest
from sqlalchemy.future import select
from trading_db.rdb.constants import Currency, StockType
from trading_db.rdb.stock.tickers import StockTicker as SAStockTicker

from pinkiepie_trading.stock.models.stock_firm import StockFirm
from pinkiepie_trading.stock.models.ticker import StockTicker
from pinkiepie_trading.stock.repositories.ticker_writer import TickerWriter


@pytest.mark.asyncio
async def test_get_by(session, firm_factory):
    # given
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    firm = await firm_factory(
        id=1, name="KB증권", trading_fee=0.1, created_at=now
    )
    ticker = StockTicker(
        id=None,
        name="apple",
        ticker="APPL",
        currency=Currency.KRW,
        stock_type=StockType.STOCK,
        fee=0.05,
        tax=0.05,
        firm=StockFirm.of(firm),
    )

    writer = TickerWriter(session)

    # when
    await writer.save(ticker)

    # then
    query = await session.execute(select(SAStockTicker))
    sa_ticker = query.scalar()

    assert sa_ticker
