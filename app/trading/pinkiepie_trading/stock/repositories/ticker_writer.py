from sqlalchemy.orm import Session
from trading_db.rdb.stock.tickers import StockTicker as SAStockTicker

from ..models.ticker import StockTicker


class TickerWriter:
    def __init__(self, session: Session):
        self.session = session

    def save(self, ticker: StockTicker):
        sa_ticker = SAStockTicker(
            stock_type=ticker.stock_type,
            name=ticker.name,
            ticker=ticker.ticker,
            currency=ticker.currency,
            fee=ticker.fee,
            tax=ticker.tax,
            firm_id=ticker.firm.id,
        )

        self.session.add(sa_ticker)
        self.session.commit()
