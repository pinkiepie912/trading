import datetime
from dataclasses import dataclass
from typing import Optional

from trading_db.rdb.stock_firm.firm import Firm as SAStockFirm


@dataclass
class StockFirm:
    id: Optional[int]
    name: str
    trading_fee: float
    created_at: datetime.datetime

    @classmethod
    def of(cls, firm: SAStockFirm):
        return cls(
            id=firm.id,
            name=firm.name,
            trading_fee=firm.trading_fee,
            created_at=firm.created_at,
        )
