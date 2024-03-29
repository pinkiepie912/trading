from __future__ import annotations

import datetime
from typing import Optional

from pydantic import BaseModel
from trading_db.rdb.stock_firm.firm import Firm as SAStockFirm

__all__ = ("StockFirm",)


class StockFirm(BaseModel):
    id: Optional[int]
    name: str
    trading_fee: float
    created_at: datetime.datetime

    @classmethod
    def of(cls, firm: SAStockFirm) -> StockFirm:
        return cls(
            id=firm.id,
            name=firm.name,
            trading_fee=firm.trading_fee,
            created_at=firm.created_at,
        )

    @classmethod
    def new(cls, name: str, trading_fee: float) -> StockFirm:
        return cls(
            name=name,
            trading_fee=trading_fee,
            created_at=datetime.datetime.now(tz=datetime.timezone.utc),
        )
