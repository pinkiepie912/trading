from typing import Optional

from sqlalchemy.orm import Session, joinedload
from trading_db.rdb.stock.tickers import StockTicker as SAStockTicker

from ..models.ticker import StockTicker


class TickerReader:
    def __init__(self, session: Session):
        self.session = session

    def get_by(self, ticker: str) -> Optional[StockTicker]:
        ticker = (
            self.session.query(SAStockTicker)
            .options(joinedload(SAStockTicker.firm))
            .filter_by(ticker=ticker)
            .first()
        )
        if not ticker:
            return None

        return StockTicker.of(ticker)