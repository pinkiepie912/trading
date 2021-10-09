from ..models.stock_firm import StockFirm
from ..models.ticker import StockTicker
from ..repositories.stock_firm_writer import StockFirmWriter
from ..repositories.ticker_writer import TickerWriter

__all__ = ("StockRegisterer",)


class StockRegisterer:
    def __init__(
        self, stock_firm_writer: StockFirmWriter, ticker_writer: TickerWriter
    ):
        self._stock_firm_writer = stock_firm_writer
        self._ticker_writer = ticker_writer

    def register_firm(self, name: str, trading_fee: float) -> None:
        stock_firm = StockFirm.new(name=name, trading_fee=trading_fee)
        self._stock_firm_writer.save(stock_firm)

    def register_ticker(
        self,
        name: str,
        ticker: str,
        currency: str,
        stock_type: str,
        fee: float,
        tax: float,
        firm: StockFirm,
    ) -> None:
        ticker = StockTicker.new(
            name=name,
            ticker=ticker,
            currency=currency,
            stock_type=stock_type,
            fee=fee,
            tax=tax,
            firm=firm,
        )
        self._ticker_writer.save(ticker)
