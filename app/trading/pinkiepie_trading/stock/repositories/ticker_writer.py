from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from trading_db.rdb.stock.tickers import StockTicker as SAStockTicker

from pinkiepie_trading.exceptions import NotFoundException

from ..models.ticker import StockTicker

__all__ = ("TickerWriter",)


class TickerWriter:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, ticker: StockTicker):
        sa_ticker = SAStockTicker(
            stock_type=ticker.stock_type,
            name=ticker.name,
            ticker=ticker.ticker,
            currency=ticker.currency,
            fee=ticker.fee,
            tax=ticker.tax,
            firm_id=ticker.firm.id,
        )

        self._session.add(sa_ticker)
        await self._session.commit()

    async def delete(self, ticker: str, soft: bool = True) -> None:
        query = select(SAStockTicker).where(SAStockTicker.ticker == ticker)

        sa_ticker = (await self._session.execute(query)).scalar()
        if not sa_ticker:
            raise NotFoundException(f"Ticker does not exist. {ticker}")

        if soft:
            sa_ticker.soft_delete()
            self._session.add(sa_ticker)
        else:
            await self._session.delete(sa_ticker)

        await self._session.commit()
