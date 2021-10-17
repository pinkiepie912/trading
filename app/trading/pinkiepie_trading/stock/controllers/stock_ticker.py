from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from pinkiepie_trading.exceptions import NotFoundException

from ..models.ticker import StockTicker
from ..schemas.stock_ticker import TickerRegistrationSchema, TickerSchema
from ..services.factory import ServiceFactory
from ..services.stock_reader import StockReader
from ..services.stock_registerer import StockRegisterer

stock_ticker_router = APIRouter(prefix="/api/stock")


@stock_ticker_router.post("/tickers", status_code=status.HTTP_201_CREATED)
async def register_stock_ticker(
    ticker: TickerRegistrationSchema,
    registerer: StockRegisterer = Depends(ServiceFactory.get_stock_registerer),
) -> Dict:
    try:
        await registerer.register_ticker(**ticker.dict())
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    return {}


@stock_ticker_router.get("/tickers", response_model=List[TickerSchema])
async def get_tickers(
    offset: int = 0,
    limit: int = 50,
    stock_reader: StockReader = Depends(ServiceFactory.get_stock_reader),
) -> List[StockTicker]:
    tickers = await stock_reader.get_tickers(offset, limit)

    return tickers
