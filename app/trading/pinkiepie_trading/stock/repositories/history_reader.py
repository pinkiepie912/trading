import datetime
from typing import List, Optional

from sqlalchemy.orm import Session
from trading_db.rdb.price import Price as SAPrice
from trading_strategy.models import Currency, Price, PriceHistory


class PriceReader:
    def __init__(self, session: Session):
        self.session = session

    def get_by(self, ticker: str, date: datetime.date) -> Optional[Price]:
        price: Optional[Price] = (
            self.session.query(SAPrice)
            .filter_by(ticker=ticker, date=date)
            .first()
        )
        if not price:
            return None

        return Price(
            ticker=price.ticker,
            currency=Currency(price.currency),
            adjclose=price.adjclose,
            close=price.close,
            date=price.date,
            high=price.high,
            low=price.low,
            open=price.open,
            volume=price.volume,
        )

    def get_history_by(
        self,
        ticker: str,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
    ) -> Optional[PriceHistory]:
        """
        include end date
        """

        end_date = end_date or datetime.date.today()
        prices_q = self.session.query(SAPrice).filter(
            SAPrice.ticker == ticker, SAPrice.date <= end_date
        )
        if start_date:
            prices_q = prices_q.filter(SAPrice.date >= start_date)

        prices: List[Price] = prices_q.order_by(SAPrice.date).all()
        if not prices:
            return None

        return PriceHistory(
            currency=Currency(prices[0].currency),
            prices=[
                Price(
                    ticker=price.ticker,
                    currency=Currency(price.currency),
                    adjclose=price.adjclose,
                    close=price.close,
                    date=price.date,
                    high=price.high,
                    low=price.low,
                    open=price.open,
                    volume=price.volume,
                )
                for price in prices
            ],
        )
