from sqlalchemy.orm import Session
from trading_db.rdb.stock.price import Price as SAPrice

from ..models.price import Price, PriceHistory

__all__ = ("PriceWriter",)


class PriceWriter:
    def __init__(self, session: Session):
        self._session = session

    def save(self, price: Price) -> None:
        sa_price = SAPrice(
            ticker_id=price.ticker_id,
            adj_close=price.adj_close,
            close=price.close,
            high=price.high,
            low=price.low,
            open=price.open,
            volume=price.volume,
            date_time=price.date_time,
            currency=price.currency,
        )

        self._session.add(sa_price)
        self._session.commit()

    def save_history(self, history=PriceHistory) -> None:
        for price in history.prices:
            self._session.add(
                SAPrice(
                    ticker_id=price.ticker_id,
                    adj_close=price.adj_close,
                    close=price.close,
                    high=price.high,
                    low=price.low,
                    open=price.open,
                    volume=price.volume,
                    date_time=price.date_time,
                    currency=price.currency,
                )
            )
        self._session.commit()
