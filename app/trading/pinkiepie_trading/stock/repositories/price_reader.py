import datetime
from typing import List

from sqlalchemy.orm import Session
from trading_db.rdb.stock.price import Price as SAPrice

from ..models.price import Price, PriceHistory
from ..models.ticker import StockTicker


class PriceReader:
    def __init__(self, session: Session):
        self.session = session

    def get_history(
        self,
        ticker: StockTicker,
        started_at: datetime.datetime,
        ended_at: datetime.datetime,
    ) -> PriceHistory:
        prices: List[SAPrice] = (
            self.session.query(SAPrice)
            .filter(
                SAPrice.ticker_id == ticker.id,
                SAPrice.date_time.between(started_at, ended_at),
            )
            .all()
        )

        return PriceHistory(
            prices=[
                Price(
                    id=price.id,
                    ticker_id=price.ticker_id,
                    adj_close=price.adj_close,
                    close=price.close,
                    date_time=price.date_time,
                    high=price.high,
                    low=price.low,
                    open=price.open,
                    volume=price.volume,
                    currency=price.currency,
                )
                for price in prices
            ],
            currency=ticker.currency,
        )
