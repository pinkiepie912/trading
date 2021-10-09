import datetime

from freezegun import freeze_time
from trading_db.rdb.stock_firm.firm import Firm as SAStockFirm

from pinkiepie_trading.stock.models.stock_firm import StockFirm


def test_of():
    # given
    sa_stock_firm = SAStockFirm(
        id=1,
        name="KB",
        trading_fee=0.1,
        created_at=datetime.datetime.now(tz=datetime.timezone.utc),
    )

    # when
    stock_firm = StockFirm.of(sa_stock_firm)

    # then
    assert stock_firm.id == sa_stock_firm.id
    assert stock_firm.name == sa_stock_firm.name
    assert stock_firm.trading_fee == sa_stock_firm.trading_fee
    assert stock_firm.created_at == sa_stock_firm.created_at


@freeze_time("2021-10-01 12:00:01")
def test_new():
    # given
    name = "KB"
    trading_fee = 0.1
    utc_now = datetime.datetime.now(tz=datetime.timezone.utc)

    # when
    stock_firm = StockFirm.new(name=name, trading_fee=trading_fee)

    # then
    assert stock_firm.name == name
    assert stock_firm.trading_fee == trading_fee
    assert stock_firm.created_at == utc_now
