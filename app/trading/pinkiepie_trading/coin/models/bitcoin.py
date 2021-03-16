import datetime

from trading_db.rdb.bitcoin import Bitcoin as SABitcoin


class BitCoin:
    def __init__(
        self,
        price: float,
        open: float,
        high: float,
        low: float,
        volume: int,
        change: float,
        date: datetime.date,
    ):
        self.price = price
        self.open = open
        self.high = high
        self.low = low
        self.volume = volume
        self.change = change
        self.date = date

    @classmethod
    def of(cls, bitcoin: SABitcoin):
        return cls(
            price=bitcoin.price,
            open=bitcoin.open,
            high=bitcoin.high,
            low=bitcoin.low,
            volume=bitcoin.volume,
            change=bitcoin.change,
            date=bitcoin.date,
        )
