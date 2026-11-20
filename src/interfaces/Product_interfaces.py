from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class IProduct(BaseModel):
    id: UUID
    name: str
    price: Decimal
    quantity: int


class IProductUpdate(BaseModel):
    name: str
    new_name: str
    price: Decimal
    quantity: int
