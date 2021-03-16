import datetime
from typing import List, Optional

from sqlalchemy import between
from sqlalchemy.orm import Session
from trading_db.rdb.bitcoin import Bitcoin as SABitcoin

from ..models.bitcoin import BitCoin


class BitcoinHistoryReaderRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by(self, target_date: datetime.date) -> Optional[BitCoin]:
        bitcoin = (
            self.session.query(SABitcoin).filter_by(date=target_date).first()
        )
        if not bitcoin:
            return None
        return BitCoin.of(bitcoin)

    def get_list_by(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> List[BitCoin]:
        history = (
            self.session.query(SABitcoin)
            .filter(between(SABitcoin.date, start_date, end_date))
            .order_by(SABitcoin.date)
            .all()
        )
        return [BitCoin.of(coin) for coin in history]
