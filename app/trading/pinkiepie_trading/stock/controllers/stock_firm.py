from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from pinkiepie_trading.database import db

from ..repositories.stock_firm_reader import StockFirmReader
from ..repositories.stock_firm_writer import StockFirmWriter
from ..repositories.ticker_reader import TickerReader
from ..repositories.ticker_writer import TickerWriter
from ..schemas.stock_firm import FirmRegistrationSchema, FirmSchema
from ..services.stock_reader import StockReader
from ..services.stock_registerer import StockRegisterer

stock_firm_router = APIRouter(prefix="/api/stock")


@stock_firm_router.post("/firms", status_code=status.HTTP_201_CREATED)
async def register_stock_firm(
    firm: FirmRegistrationSchema,
    session: AsyncSession = Depends(db.get_session),
):
    registerer = StockRegisterer(
        stock_firm_writer=StockFirmWriter(session),
        ticker_writer=TickerWriter(session),
    )

    await registerer.register_firm(
        name=firm.name, trading_fee=firm.trading_fee
    )
    return {}


@stock_firm_router.get("/firms", response_model=List[FirmSchema])
async def get_firms(
    offset: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(db.get_session),
):
    reader = StockReader(
        stock_firm_reader=StockFirmReader(session),
        ticker_reader=TickerReader(session),
    )

    firms = await reader.get_stock_firms(offset, limit)

    return firms
