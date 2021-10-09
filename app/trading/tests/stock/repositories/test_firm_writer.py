import datetime

import pytest
from sqlalchemy import select
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
