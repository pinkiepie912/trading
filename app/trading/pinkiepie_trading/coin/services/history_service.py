import datetime

from ..repositories.history_reader import BitcoinHistoryReaderRepository


class BitcoinHistoryService:
    def __init__(self, repository: BitcoinHistoryReaderRepository):
        self.repository = repository

    def get_by(self, target_date: datetime.date):
        history = self.repository.get_by(target_date)
        return history

    def get_list_by(self, start_date: datetime.date, end_date: datetime.date):
        history = self.repository.get_list_by(start_date, end_date)
        return history
