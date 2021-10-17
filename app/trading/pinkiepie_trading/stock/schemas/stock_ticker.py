from pydantic import BaseModel
from trading_db.rdb.constants import Currency, StockType

from .stock_firm import FirmSchema

__all__ = ("TickerRegistrationSchema", "TickerSchema")


class TickerRegistrationSchema(BaseModel):
    stock_type: StockType
    name: str
    ticker: str
    currency: Currency
    firm_id: int
    fee: float
    tax: float


class TickerSchema(BaseModel):
    id: int
    stock_type: StockType
    name: str
    ticker: str
    currency: Currency
    firm: FirmSchema
    fee: float
    tax: float
