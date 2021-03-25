import datetime

from trading_db.rdb.price import Price as SAPrice
from trading_strategy.models import Currency, Price, PriceHistory

from pinkiepie_trading.stock.repositories.history_writer import PriceWriter


def test_save(session):
    # givne
    name = "apple"
    ticker = "APPL"
    today = datetime.date.today()
    price = Price(
        ticker=ticker,
        currency=Currency.USD,
        adjclose=100.1,
        close=100.1,
        high=110.1,
        low=90.1,
        open=95.1,
        volume=100000,
        date=today,
    )

    writer = PriceWriter(session)

    # when
    writer.save(price, name)

    # then
    sa_price = session.query(SAPrice).filter(SAPrice.ticker == ticker).first()

    assert sa_price
    assert sa_price.date == price.date


def test_save_history(session):
    # givne
    name = "apple"
    ticker = "APPL"
    today = datetime.date.today()

    history_length = 10
    history = PriceHistory(
        name=name,
        ticker=ticker,
        currency=Currency.USD,
        prices=[
            Price(
                ticker=ticker,
                currency=Currency.USD,
                adjclose=100.1,
                close=100.1,
                high=110.1,
                low=90.1,
                open=95.1,
                volume=100000,
                date=today,
            )
            for _ in range(history_length)
        ],
    )

    writer = PriceWriter(session)

    # when
    writer.save_history(history)

    # then
    price_cnt = session.query(SAPrice).filter(SAPrice.ticker == ticker).count()

    assert price_cnt == history_length
