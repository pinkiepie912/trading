from trading_db.rdb.constants import Currency, StockType

from pinkiepie_trading.stock.repositories.ticker_reader import TickerReader


def test_get_by(session, firm_factory, ticker_factory):
    # given
    target_ticker = "APPL"
    firm = firm_factory(id=1, name="KB증권", trading_fee=0.1)
    ticker_factory(
        stock_type=StockType.STOCK,
        name="apple",
        ticker=target_ticker,
        firm=firm,
        fee=0.05,
        tax=0.05,
        currency=Currency.KRW,
    )

    reader = TickerReader(session)

    # when
    ticker = reader.get_by(target_ticker)

    # then
    assert ticker


def test_get_by_no_ticker(session):
    # given
    ticker = "NOTICKER"
    reader = TickerReader(session)

    # when, then
    assert not reader.get_by(ticker)
