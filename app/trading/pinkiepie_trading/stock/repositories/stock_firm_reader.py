from typing import List

from sqlalchemy.orm import Session
from trading_db.rdb.stock_firm.firm import Firm as SAStockFirm

from ..models.stock_firm import StockFirm

__all__ = ("StockFirmReader",)


class StockFirmReader:
    def __init__(self, session: Session):
        self.session = session

    def get_list(self, offset: int = 0, limit: int = 10) -> List[StockFirm]:
        firms = (
            self.session.query(SAStockFirm)
            .order_by(SAStockFirm.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return [StockFirm.of(firm) for firm in firms]
