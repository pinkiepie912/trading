from typing import List

from pinkiepie_trading.exceptions import NotFoundException

from ..models.stock_firm import StockFirm
from ..models.ticker import StockTicker
from ..repositories.stock_firm_reader import StockFirmReader
from ..repositories.ticker_reader import TickerReader

__all__ = ("StockReader",)


class StockReader:
    def __init__(
        self, stock_firm_reader: StockFirmReader, ticker_reader: TickerReader
    ):
        self._stock_firm_reader = stock_firm_reader
        self._ticker_reader = ticker_reader

    async def get_stock_firm(self, id_: int):
        return await self._stock_firm_reader.get_by(id_)

    async def get_stock_firms(
        self, offset: int = 0, limit: int = 10
    ) -> List[StockFirm]:
        return await self._stock_firm_reader.get_list(offset, limit)

    async def get_tickers(
        self, offset: int = 0, limit: int = 10
    ) -> List[StockTicker]:
        return await self._ticker_reader.get_list(offset, limit)

    async def get_ticker(self, ticker: str) -> StockTicker:
        ticker_obj = await self._ticker_reader.get_by(ticker)
        if not ticker_obj:
            raise NotFoundException(f"{ticker} does not exist")

        return ticker_obj
