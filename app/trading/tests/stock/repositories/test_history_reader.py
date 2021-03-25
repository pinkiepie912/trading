import datetime

from trading_db.rdb.price import Currency

from pinkiepie_trading.stock.repositories.history_reader import PriceReader


def test_get_by(session, price_factory):
    # given
    target_ticker = "AAPL"
    today = datetime.date.today()
    target_price = price_factory(
        name="apple",
        ticker=target_ticker,
        adjclose=100.1,
        close=100.1,
        high=110.1,
        low=90.1,
        open=95.1,
        volume=100000,
        date=today,
        currency=Currency.USD.value,
    )

    # non target price
    yesterday = today - datetime.timedelta(days=1)
    price_factory(
        name="apple",
        ticker=target_ticker,
        adjclose=100.1,
        close=100.1,
        high=110.1,
        low=90.1,
        open=95.1,
        volume=100000,
        date=yesterday,
        currency=Currency.USD.value,
    )

    reader = PriceReader(session)

    # when
    price = reader.get_by(target_ticker, today)

    # then
    assert price.date == target_price.date


def test_get_history_by(session, price_factory):
    # given
    history_length = 10
    target_ticker = "AAPL"

    today = datetime.date.today()
    expected_length = 5
    start_date = today - datetime.timedelta(days=expected_length)
    end_date = today

    for i in range(1, history_length):
        price_factory(
            name="apple",
            ticker=target_ticker,
            adjclose=100.1,
            close=100.1,
            high=110.1,
            low=90.1,
            open=95.1,
            volume=100000,
            date=today - datetime.timedelta(days=i),
            currency=Currency.USD.value,
        )

    reader = PriceReader(session)

    # when
    history = reader.get_history_by(target_ticker, start_date, end_date)

    # then
    assert history.currency.name == Currency.USD.name
    assert len(history.prices) == expected_length
