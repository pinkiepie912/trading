import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from trading_db.rdb.stock.price import Price as SAPrice

from ..models.price import Price, PriceHistory
from ..models.ticker import StockTicker

__all__ = ("PriceReader",)


class PriceReader:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_history(
        self,
        ticker: StockTicker,
        started_at: datetime.datetime,
        ended_at: datetime.datetime,
    ) -> PriceHistory:

        query = select(SAPrice).where(
            SAPrice.ticker_id == ticker.id,
            SAPrice.date_time.between(started_at, ended_at),
        )
        prices = await self._session.execute(query)

        return PriceHistory(
            prices=[
                Price(
                    id=price.id,
                    ticker_id=price.ticker_id,
                    adj_close=price.adj_close,
                    close=price.close,
                    date_time=price.date_time,
                    high=price.high,
                    low=price.low,
                    open=price.open,
                    volume=price.volume,
                    currency=price.currency,
                )
                for price in prices.scalars()
            ],
            currency=ticker.currency,
        )
