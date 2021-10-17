from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from pinkiepie_trading.database import db

from ..repositories.stock_firm_reader import StockFirmReader
from ..repositories.stock_firm_writer import StockFirmWriter
from ..repositories.ticker_reader import TickerReader
from ..repositories.ticker_writer import TickerWriter
from ..services.stock_reader import StockReader
from ..services.stock_registerer import StockRegisterer


class ServiceFactory:
    @classmethod
    def get_stock_reader(
        cls, session: AsyncSession = Depends(db.get_session)
    ) -> StockReader:
        return StockReader(
            stock_firm_reader=StockFirmReader(session),
            ticker_reader=TickerReader(session),
        )

    @classmethod
    def get_stock_registerer(
        cls, session: AsyncSession = Depends(db.get_session)
    ) -> StockRegisterer:
        return StockRegisterer(
            stock_firm_writer=StockFirmWriter(session),
            ticker_writer=TickerWriter(session),
            stock_reader=cls.get_stock_reader(session),
        )
