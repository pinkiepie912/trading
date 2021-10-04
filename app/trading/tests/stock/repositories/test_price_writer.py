import datetime

from trading_db.rdb.constants import Currency, StockType
from trading_db.rdb.stock.price import Price as SAPrice

from pinkiepie_trading.stock.models.price import Price, PriceHistory
from pinkiepie_trading.stock.repositories.price_writer import PriceWriter


def test_save(request, session, firm_factory, ticker_factory):
    # given
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    firm = firm_factory(name="KB증권", trading_fee=0.1)
    ticker = ticker_factory(
        stock_type=StockType.STOCK,
        name="apple",
        ticker="APPL",
        firm=firm,
        fee=0.05,
        tax=0.05,
        currency=Currency.KRW,
    )
    session.add(firm)
    session.add(ticker)
    session.commit()

    price = Price(
        id=None,
        adj_close=100.1,
        close=100.1,
        high=110.1,
        low=90.1,
        open=95.1,
        volume=100000,
        date_time=now,
        ticker_id=ticker.id,
        currency=Currency.USD,
    )

    writer = PriceWriter(session)

    # when
    writer.save(price)

    # then
    sa_price = session.query(SAPrice).filter(SAPrice.ticker == ticker).first()

    assert sa_price

    @request.addfinalizer
    def teardown():
        session.delete(sa_price)
        session.delete(ticker)
        session.delete(firm)

        session.commit()


def test_save_history(request, session, firm_factory, ticker_factory):
    # given
    now = datetime.datetime.now(tz=datetime.timezone.utc)

    firm = firm_factory(name="KB증권", trading_fee=0.1)
    ticker = ticker_factory(
        stock_type=StockType.STOCK,
        name="apple",
        ticker="APPL",
        firm=firm,
        fee=0.05,
        tax=0.05,
        currency=Currency.KRW,
    )
    session.add(firm)
    session.add(ticker)
    session.commit()

    history_length = 10
    history = PriceHistory(
        currency=Currency.USD,
        prices=[
            Price(
                id=None,
                adj_close=100.1,
                close=100.1,
                high=110.1,
                low=90.1,
                open=95.1,
                volume=100000,
                date_time=now + datetime.timedelta(hours=i),
                ticker_id=ticker.id,
                currency=Currency.USD,
            )
            for i in range(history_length)
        ],
    )

    writer = PriceWriter(session)

    # when
    writer.save_history(history)

    # then
    prices = session.query(SAPrice).filter(SAPrice.ticker == ticker).all()

    assert len(prices) == history_length

    @request.addfinalizer
    def teardown():
        for price in prices:
            session.delete(price)
        session.delete(ticker)
        session.delete(firm)

        session.commit()
