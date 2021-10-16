from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from trading_db.rdb.stock.tickers import StockTicker as SAStockTicker

from ..models.ticker import StockTicker

__all__ = ("TickerReader",)


class TickerReader:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_list(
        self, offset: int = 0, limit: int = 10
    ) -> List[StockTicker]:
        query = await self._session.execute(
            select(SAStockTicker)
            .options(joinedload(SAStockTicker.firm))
            .where(SAStockTicker.is_active)
            .offset(offset)
            .limit(limit)
        )
        return [StockTicker.of(ticker) for ticker in query.scalars().all()]

    async def get_by(self, ticker: str) -> Optional[StockTicker]:
        query = await self._session.execute(
            select(SAStockTicker)
            .options(joinedload(SAStockTicker.firm))
            .where(SAStockTicker.is_active)
            .filter_by(ticker=ticker)
        )
        ticker = query.scalar()

        if not ticker:
            return None

        return StockTicker.of(ticker)
