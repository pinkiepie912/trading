from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from trading_db.rdb.constants import Currency, StockType
from trading_db.rdb.stock.tickers import StockTicker as SAStockTicker

from .stock_firm import StockFirm

__all__ = ("StockTicker",)


class StockTicker(BaseModel):
    id: Optional[int]
    name: str
    ticker: str
    currency: Currency
    stock_type: StockType
    fee: float
    tax: float
    firm: StockFirm

    @classmethod
    def of(cls, ticker: SAStockTicker) -> StockTicker:
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

    @classmethod
    def new(
        cls,
        name: str,
        ticker: str,
        currency: str,
        stock_type: str,
        fee: float,
        tax: float,
        firm: StockFirm,
    ) -> StockTicker:
        try:
            _currency = Currency(currency)
        except ValueError:
            raise ValueError(f"{currency} is invalid currency")

        try:
            _stock_type = StockType(stock_type)
        except ValueError:
            raise ValueError(f"{stock_type} is invalid stock type")

        return cls(
            name=name,
            ticker=ticker,
            currency=_currency,
            stock_type=_stock_type,
            fee=fee,
            tax=tax,
            firm=firm,
        )
