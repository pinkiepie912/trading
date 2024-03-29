from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from pinkiepie_trading.exceptions import NotFoundException

from ..models.stock_firm import StockFirm
from ..schemas.stock_firm import FirmRegistrationSchema, FirmSchema
from ..services.factory import ServiceFactory
from ..services.stock_reader import StockReader
from ..services.stock_registerer import StockRegisterer

stock_firm_router = APIRouter(prefix="/api/stock")


@stock_firm_router.post("/firms", status_code=status.HTTP_201_CREATED)
async def register_stock_firm(
    firm: FirmRegistrationSchema,
    registerer: StockRegisterer = Depends(ServiceFactory.get_stock_registerer),
) -> Dict:
    await registerer.register_firm(
        name=firm.name, trading_fee=firm.trading_fee
    )
    return {}


@stock_firm_router.get("/firms", response_model=List[FirmSchema])
async def get_firms(
    offset: int = 0,
    limit: int = 10,
    reader: StockReader = Depends(ServiceFactory.get_stock_reader),
) -> List[StockFirm]:
    firms = await reader.get_stock_firms(offset, limit)

    return firms


@stock_firm_router.delete("/firms/{firm_id}", status_code=status.HTTP_200_OK)
async def delete(
    firm_id: int,
    registerer: StockRegisterer = Depends(ServiceFactory.get_stock_registerer),
) -> Dict:
    try:
        await registerer.delete_firm(firm_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    return {}
