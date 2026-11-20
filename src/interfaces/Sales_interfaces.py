from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class ISale(BaseModel):
    product_id: UUID
    quantity: int
    value: Decimal
