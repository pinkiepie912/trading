from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass
from typing import List

from trading_db.rdb.constants import Currency
from yahoofinancials import YahooFinancials

from .exceptions import (
    InvalidPeriodError,
    InvalidTickerError,
    NoHistoricalDataError,
)
from .utils import date_to_str


class Interval(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class YahooFinanceClient:
    def __init__(self):
        super().__init__()

    def get_historical_data(
        self,
        ticker: str,
        start_date: datetime.date,
        end_date: datetime.date,
        time_interval: Interval,
    ) -> YFPriceHistory:
        if start_date > end_date:
            raise InvalidPeriodError

        yahoo_financial = YahooFinancials(ticker)
        data = yahoo_financial.get_historical_price_data(
            start_date=date_to_str(start_date),
            end_date=date_to_str(end_date),
            time_interval=time_interval.value,
        )

        data = data[ticker]
        if "prices" not in data:
            raise InvalidTickerError

        prices = data["prices"]
        if not prices:
            raise NoHistoricalDataError

        time_offset = data["timeZone"]["gmtOffset"]

        return YFPriceHistory.create(
            prices=prices,
            time_offset=time_offset,
            currency=Currency(data["currency"]),
        )


@dataclass
class YFPriceHistory:
    prices: List[YFPrice]
    currency: Currency

    @classmethod
    def create(cls, prices: List[dict], time_offset: int, currency: Currency):
        return cls(
            prices=[
                YFPrice(
                    adj_close=price["adjclose"],
                    close=price["close"],
                    date_time=datetime.datetime.fromtimestamp(
                        price["date"] - time_offset, tz=datetime.timezone.utc
                    ),
                    high=price["high"],
                    low=price["low"],
                    open=price["open"],
                    volume=price["volume"],
                )
                for price in prices
            ],
            currency=currency,
        )


@dataclass
class YFPrice:
    adj_close: float
    close: float
    date_time: datetime.datetime
    high: float
    low: float
    open: float
    volume: int
