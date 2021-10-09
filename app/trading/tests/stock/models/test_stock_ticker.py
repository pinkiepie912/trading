import datetime

import pytest
from trading_db.rdb.constants import Currency, StockType
from trading_db.rdb.stock.tickers import StockTicker as SAStockTicker
from trading_db.rdb.stock_firm.firm import Firm as SAStockFirm

from pinkiepie_trading.stock.models.stock_firm import StockFirm
from pinkiepie_trading.stock.models.ticker import StockTicker


def test_of():
    # given
    sa_stock_firm = SAStockFirm(
        id=1,
        name="KB",
        trading_fee=0.1,
        created_at=datetime.datetime.now(tz=datetime.timezone.utc),
    )

    sa_stock_ticker = SAStockTicker(
        name="Apple",
        ticker="APPL",
        stock_type=StockType.STOCK,
        currency=Currency.USD,
        fee=0.1,
        tax=0.1,
        firm_id=sa_stock_firm.id,
        firm=sa_stock_firm,
    )

    # when
    ticker = StockTicker.of(sa_stock_ticker)

    # then
    assert ticker.name == sa_stock_ticker.name
    assert ticker.ticker == sa_stock_ticker.ticker
    assert ticker.currency == sa_stock_ticker.currency
    assert ticker.stock_type == sa_stock_ticker.stock_type
    assert ticker.fee == sa_stock_ticker.fee
    assert ticker.tax == sa_stock_ticker.tax

    assert ticker.firm.id == sa_stock_firm.id
    assert ticker.firm.name == sa_stock_firm.name
    assert ticker.firm.trading_fee == sa_stock_firm.trading_fee
    assert ticker.firm.created_at == sa_stock_firm.created_at


def test_new():
    # given
    name = "Apple"
    ticker = "APPL"
    currency = Currency.USD
    stock_type = StockType.STOCK
    fee = 0.1
    tax = 0.1
    stock_firm = StockFirm(
        id=1,
        name="KB",
        trading_fee=0.1,
        created_at=datetime.datetime.now(tz=datetime.timezone.utc),
    )

    # when
    ticker = StockTicker.new(
        name=name,
        ticker=ticker,
        currency=currency.value,
        stock_type=stock_type.value,
        fee=fee,
        tax=tax,
        firm=stock_firm,
    )

    # then
    assert ticker.name == name
    assert ticker.currency == currency
    assert ticker.stock_type == stock_type
    assert ticker.fee == fee
    assert ticker.tax == tax

    assert ticker.firm.id == stock_firm.id
    assert ticker.firm.name == stock_firm.name
    assert ticker.firm.trading_fee == stock_firm.trading_fee
    assert ticker.firm.created_at == stock_firm.created_at


def test_new_invalid_currency():
    # given
    name = "Apple"
    ticker = "APPL"
    invalid_currency = "INVALID"
    stock_type = StockType.STOCK
    fee = 0.1
    tax = 0.1
    stock_firm = StockFirm(
        id=1,
        name="KB",
        trading_fee=0.1,
        created_at=datetime.datetime.now(tz=datetime.timezone.utc),
    )

    # when, then
    with pytest.raises(ValueError, match=".* is invalid currency"):
        StockTicker.new(
            name=name,
            ticker=ticker,
            currency=invalid_currency,
            stock_type=stock_type.value,
            fee=fee,
            tax=tax,
            firm=stock_firm,
        )


def test_new_invalid_stock_type():
    # given
    name = "Apple"
    ticker = "APPL"
    currency = Currency.USD
    invalid_stock_type = "INVALID"
    fee = 0.1
    tax = 0.1
    stock_firm = StockFirm(
        id=1,
        name="KB",
        trading_fee=0.1,
        created_at=datetime.datetime.now(tz=datetime.timezone.utc),
    )

    # when, then
    with pytest.raises(ValueError, match=".* is invalid stock type"):
        StockTicker.new(
            name=name,
            ticker=ticker,
            currency=currency.value,
            stock_type=invalid_stock_type,
            fee=fee,
            tax=tax,
            firm=stock_firm,
        )
