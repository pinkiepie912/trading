from dataclasses import dataclass
from typing import Optional

from trading_db.rdb.constants import Currency, StockType
from trading_db.rdb.stock.tickers import StockTicker as SAStockTicker

from .stock_firm import StockFirm


@dataclass
class StockTicker:
    id: Optional[int]
    name: str
    ticker: str
    currency: Currency
    stock_type: StockType
    fee: float
    tax: float
    firm: StockFirm

    @classmethod
    def of(cls, ticker: SAStockTicker):
        return cls(
            id=ticker.id,
            name=ticker.name,
            ticker=ticker.ticker,
            currency=ticker.currency,
            stock_type=ticker.stock_type,
            fee=ticker.fee,
            tax=ticker.tax,
            firm=StockFirm.of(ticker.firm),
        )
