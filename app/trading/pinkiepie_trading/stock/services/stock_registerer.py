from ..models.stock_firm import StockFirm
from ..models.ticker import StockTicker
from ..repositories.stock_firm_writer import StockFirmWriter
from ..repositories.ticker_writer import TickerWriter
from .stock_reader import StockReader

__all__ = ("StockRegisterer",)


class StockRegisterer:
    def __init__(
        self,
        stock_firm_writer: StockFirmWriter,
        ticker_writer: TickerWriter,
        stock_reader: StockReader,
    ):
        self._stock_reader = stock_reader
        self._stock_firm_writer = stock_firm_writer
        self._ticker_writer = ticker_writer

    async def register_firm(self, name: str, trading_fee: float) -> None:
        stock_firm = StockFirm.new(name=name, trading_fee=trading_fee)
        await self._stock_firm_writer.save(stock_firm)

    async def delete_firm(self, id_: int) -> None:
        await self._stock_firm_writer.delete(id_),

    async def register_ticker(
        self,
        name: str,
        ticker: str,
        currency: str,
        stock_type: str,
        fee: float,
        tax: float,
        firm_id: int,
    ) -> None:
        firm = await self._stock_reader.get_stock_firm(firm_id)
        ticker = StockTicker.new(
            name=name,
            ticker=ticker,
            currency=currency,
            stock_type=stock_type,
            fee=fee,
            tax=tax,
            firm=firm,
        )
        await self._ticker_writer.save(ticker)

    async def delete_ticker(self, ticker: str) -> None:
        await self._ticker_writer.delete(ticker)
