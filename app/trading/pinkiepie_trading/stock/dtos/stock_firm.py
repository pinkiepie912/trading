from pydantic import BaseModel

__all__ = ("FirmRegistrationSchema", "FirmSchema")


class FirmRegistrationSchema(BaseModel):
    name: str
    trading_fee: float


class FirmSchema(BaseModel):
    id: int
    name: str
    trading_fee: float
