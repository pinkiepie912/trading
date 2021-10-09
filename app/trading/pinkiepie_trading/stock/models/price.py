import datetime
from typing import List, Optional

from pydantic import BaseModel
from trading_db.rdb.constants import Currency

from pinkiepie_trading.constants import TZ_SEOUL


class Price(BaseModel):
    id: Optional[int]
    ticker_id: int
    adj_close: float
    close: float
    date_time: datetime.datetime
    high: float
    low: float
    open: float
    volume: int
    currency: Currency

    @property
    def date_time_kst(self) -> datetime.datetime:
        return self.date_time.astimezone(TZ_SEOUL)


class PriceHistory(BaseModel):
    prices: List[Price]
    currency: Currency
