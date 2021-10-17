from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from trading_db.rdb.stock_firm.firm import Firm as SAStockFirm

from pinkiepie_trading.exceptions import NotFoundException

from ..models.stock_firm import StockFirm

__all__ = ("StockFirmReader",)


class StockFirmReader:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by(self, id_: int) -> StockFirm:
        query = select(SAStockFirm).where(SAStockFirm.id == id_)

        firm = (await self._session.execute(query)).scalar()
        if not firm:
            raise NotFoundException(f"Firm {id_} does not exist")

        return StockFirm.of(firm)

    async def get_list(
        self, offset: int = 0, limit: int = 10
    ) -> List[StockFirm]:
        query = (
            select(SAStockFirm)
            .order_by(SAStockFirm.created_at.desc())
            .where(SAStockFirm.is_active)
            .offset(offset)
            .limit(limit)
        )
        firms = await self._session.execute(query)
        return [StockFirm.of(firm) for firm in firms.scalars().all()]
