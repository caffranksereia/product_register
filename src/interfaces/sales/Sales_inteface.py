from uuid import UUID

from pydantic import BaseModel, Field


class ISale(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)
