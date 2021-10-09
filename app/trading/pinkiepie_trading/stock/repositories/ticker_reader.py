from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from trading_db.rdb.stock.tickers import StockTicker as SAStockTicker

from ..models.ticker import StockTicker

__all__ = ("TickerReader",)


class TickerReader:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by(self, ticker: str) -> Optional[StockTicker]:
        query = await self._session.execute(
            select(SAStockTicker)
            .options(joinedload(SAStockTicker.firm))
            .filter_by(ticker=ticker)
        )
        ticker = query.scalar()

        if not ticker:
            return None

        return StockTicker.of(ticker)
