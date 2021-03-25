from sqlalchemy.orm import Session
from trading_db.rdb.price import Price as SAPrice
from trading_strategy.models import Price, PriceHistory


class PriceWriter:
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def save(self, price: Price, name: str) -> Price:
        sa_price = SAPrice(
            name=name,
            ticker=price.ticker,
            currency=price.currency.value,
            adjclose=price.adjclose,
            close=price.close,
            date=price.date,
            high=price.high,
            low=price.low,
            open=price.open,
            volume=price.volume,
        )

        self.session.add(sa_price)
        self.session.commit()

        return price

    def save_history(self, history=PriceHistory) -> PriceHistory:
        for price in history.prices:
            self.session.add(
                SAPrice(
                    name=history.name,
                    ticker=price.ticker,
                    currency=price.currency.value,
                    adjclose=price.adjclose,
                    close=price.close,
                    date=price.date,
                    high=price.high,
                    low=price.low,
                    open=price.open,
                    volume=price.volume,
                )
            )

        self.session.commit()
        return history
