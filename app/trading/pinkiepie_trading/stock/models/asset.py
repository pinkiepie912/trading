from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from trading_db.rdb.asset.stock import StockAsset as SAStockAsset
from trading_db.rdb.constants import Currency

from .ticker import StockTicker


class StockAsset(BaseModel):
    id: Optional[int]
    ticker_id: int
    description: str
    currency: Currency
    purchase_price: float
    purchased_at: datetime
    amount: int
    sell_price: float
    sold_at: Optional[datetime]
    has_not_yet_sold: bool

    ticker: Optional[StockTicker]

    @property
    def purchase_cost(self) -> float:
        return self.purchase_price * self.amount

    @classmethod
    def of(cls, asset: SAStockAsset) -> StockAsset:
        return cls(
            id=asset.id,
            ticker_id=asset.ticker_id,
            description=asset.description,
            currency=asset.currency,
            purchase_price=asset.purchase_price,
            purchased_at=asset.purchased_at,
            amount=asset.amount,
            sell_price=asset.sell_price,
            sold_at=asset.sold_at,
            has_not_yet_sold=asset.has_not_yet_sold,
            ticker=StockTicker.of(asset.ticker),
        )
