from uuid import UUID

from pydantic import BaseModel


class IProduct(BaseModel):
    id: UUID
    name: str
    price: int
    quantity: int
