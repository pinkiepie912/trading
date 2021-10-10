from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from pinkiepie_trading.database import db

from ..dtos.stock_firm import FirmRegistrationSchema
from ..repositories.stock_firm_writer import StockFirmWriter
from ..repositories.ticker_writer import TickerWriter
from ..services.stock_registerer import StockRegisterer

stock_firm_router = APIRouter(prefix="/api/stock")


@stock_firm_router.post("/firm", status_code=status.HTTP_201_CREATED)
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
