from sqlalchemy.orm import Session
from trading_db.rdb.stock_firm.firm import Firm as SAStockFirm

from ..models.stock_firm import StockFirm

__all__ = ("StockFirmWriter",)


class StockFirmWriter:
    def __init__(self, session: Session):
        self._session = session

    def save(self, firm: StockFirm) -> None:
        sa_firm = SAStockFirm(
            name=firm.name,
            trading_fee=firm.trading_fee,
            created_at=firm.created_at,
        )

        self._session.add(sa_firm)
        self._session.commit()
