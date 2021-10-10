from pydantic import BaseModel

__all__ = ("FirmRegistrationSchema",)


class FirmRegistrationSchema(BaseModel):
    name: str
    trading_fee: float
