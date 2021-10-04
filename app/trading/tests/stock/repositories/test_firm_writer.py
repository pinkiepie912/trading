import datetime

from trading_db.rdb.stock_firm.firm import Firm as SAStockFirm

from pinkiepie_trading.stock.models.stock_firm import StockFirm
from pinkiepie_trading.stock.repositories.stock_firm_writer import (
    StockFirmWriter,
)


def test_get_list(request, session):
    # given
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    stock_firm = StockFirm(
        id=None, name="KB증권", trading_fee=0.1, created_at=now
    )

    writer = StockFirmWriter(session)

    # when
    writer.save(stock_firm)

    # then
    sa_stock_firm = (
        session.query(SAStockFirm).filter_by(name=stock_firm.name).first()
    )
    assert sa_stock_firm

    @request.addfinalizer
    def teardown():
        session.delete(sa_stock_firm)
