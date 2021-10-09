from trading_db.rdb.constants import Currency, StockType
from trading_db.rdb.stock.tickers import StockTicker as SAStockTicker
from trading_db.rdb.stock_firm.firm import Firm as SAStockFirm

from pinkiepie_trading.stock.models.stock_firm import StockFirm
from pinkiepie_trading.stock.repositories.stock_firm_writer import (
    StockFirmWriter,
)
from pinkiepie_trading.stock.repositories.ticker_writer import TickerWriter
from pinkiepie_trading.stock.services.stock_registerer import StockRegisterer


def test_register_firm(request, session):
    # given
    name = "KB증권"
    trading_fee = 0.1

    stock_firm_writer = StockFirmWriter(session)
    ticker_writer = TickerWriter(session)
    registerer = StockRegisterer(stock_firm_writer, ticker_writer)

    # when
    registerer.register_firm(name=name, trading_fee=trading_fee)

    # then
    sa_stock_firm = session.query(SAStockFirm).filter_by(name=name).first()

    assert sa_stock_firm

    @request.addfinalizer
    def teardown():
        session.delete(sa_stock_firm)


def test_register_ticker(request, session, firm_factory):
    # given
    name = "apple"
    ticker = "APPL"
    currency = Currency.KRW
    stock_type = StockType.STOCK
    fee = 0.05
    tax = 0.05
    stock_firm = StockFirm.of(firm_factory(name="KB증권", trading_fee=0.1))

    stock_firm_writer = StockFirmWriter(session)
    ticker_writer = TickerWriter(session)
    registerer = StockRegisterer(stock_firm_writer, ticker_writer)

    # when
    registerer.register_ticker(
        name=name,
        ticker=ticker,
        currency=currency.value,
        stock_type=stock_type.value,
        fee=fee,
        tax=tax,
        firm=stock_firm,
    )

    # then
    sa_stock_ticker = session.query(SAStockTicker).filter_by(name=name).first()

    assert sa_stock_ticker

    @request.addfinalizer
    def teardown():
        session.delete(sa_stock_ticker)
