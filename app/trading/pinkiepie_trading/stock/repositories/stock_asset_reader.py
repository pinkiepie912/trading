from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import func
from trading_db.rdb.asset.stock import StockAsset as SAStockAsset
from trading_db.rdb.stock.tickers import StockTicker as SAStockTicker

from ..models.asset import StockAsset

__all__ = ("StockAssetReader",)


class StockAssetReader:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_count(self, has_not_yet_sold_only: bool = False) -> int:
        query = select(func.count(SAStockAsset.id)).where(
            SAStockAsset.is_active
        )
        if has_not_yet_sold_only:
            query = query.where(SAStockAsset.has_not_yet_sold)

        return (await self._session.execute(query)).scalar()

    async def get_assets(
        self,
        offset: int = 0,
        limit: int = 50,
        has_not_yet_sold_only: bool = False,
    ) -> List[StockAsset]:
        query = select(SAStockAsset).where(SAStockAsset.is_active)
        if has_not_yet_sold_only:
            query = query.where(SAStockAsset.has_not_yet_sold)

        query = (
            query.options(
                joinedload(SAStockAsset.ticker, innerjoin=True).joinedload(
                    SAStockTicker.firm, innerjoin=True
                )
            )
            .order_by(SAStockAsset.purchased_at.desc())
            .offset(offset)
            .limit(limit)
        )

        assets: List[SAStockAsset] = (
            (await self._session.execute(query)).scalars().all()
        )
        return [StockAsset.of(asset) for asset in assets]
