from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from trading_db.rdb.stock_firm.firm import Firm as SAStockFirm

from pinkiepie_trading.exceptions import NotFoundException

from ..models.stock_firm import StockFirm

__all__ = ("StockFirmWriter",)


class StockFirmWriter:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, firm: StockFirm) -> None:
        sa_firm = SAStockFirm(
            name=firm.name,
            trading_fee=firm.trading_fee,
            created_at=firm.created_at,
        )

        self._session.add(sa_firm)
        await self._session.commit()

    async def delete(self, firm_id: int, soft: bool = True) -> None:
        query = (
            select(SAStockFirm)
            .options(joinedload(SAStockFirm.tickers))
            .where(SAStockFirm.id == firm_id)
        )
        sa_firm = (await self._session.execute(query)).scalar()
        if not sa_firm:
            raise NotFoundException(f"Firm does not exist. id: {firm_id}")

        if soft:
            sa_firm.soft_delete()
            self._session.add(sa_firm)
        else:
            await self._session.delete(sa_firm)

        await self._session.commit()
