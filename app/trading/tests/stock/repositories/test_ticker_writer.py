from trading_db.rdb.constants import Currency, StockType
from trading_db.rdb.stock.tickers import StockTicker as SAStockTicker

from pinkiepie_trading.stock.models.stock_firm import StockFirm
from pinkiepie_trading.stock.models.ticker import StockTicker
from pinkiepie_trading.stock.repositories.ticker_writer import TickerWriter


def test_get_by(request, session, firm_factory):
    # given
    firm = firm_factory(id=1, name="KB증권", trading_fee=0.1)
    session.add(firm)
    session.commit()

    ticker = StockTicker(
        id=None,
        name="apple",
        ticker="APPL",
        currency=Currency.KRW,
        stock_type=StockType.STOCK,
        fee=0.05,
        tax=0.05,
        firm=StockFirm.of(firm),
    )

    writer = TickerWriter(session)

    # when
    writer.save(ticker)

    # then
    sa_ticker = session.query(SAStockTicker).first()
    assert ticker

    @request.addfinalizer
    def teardown():
        session.delete(sa_ticker)
