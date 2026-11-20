from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class IProduct(BaseModel):
    id: UUID
    name: str
    price: Decimal
    quantity: int
